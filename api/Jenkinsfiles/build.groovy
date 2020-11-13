#!/usr/bin/env groovy
// Copyright © 2018 Province of British Columbia
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

//JENKINS DEPLOY ENVIRONMENT VARIABLES:
// - JENKINS_JAVA_OVERRIDES  -Dhudson.model.DirectoryBrowserSupport.CSP= -Duser.timezone=America/Vancouver
//   -> user.timezone : set the local timezone so logfiles report correxct time
//   -> hudson.model.DirectoryBrowserSupport.CSP : removes restrictions on CSS file load, thus html pages of test reports are displayed pretty
//   See: https://docs.openshift.com/container-platform/3.9/using_images/other_images/jenkins.html for a complete list of JENKINS env vars

// define constants
def BUILDCFG_BASE ='namex-api-base'
def IMAGE_BASE_NAME = 'namex-api-base'

def BUILDCFG_RUNTIME ='namex-api-runtime'
def IMAGE_RUNTIME_NAME = 'namex-api-runtime'

def DEV_DEPLOYMENT_NAME = 'namex-api'
def DEV_TAG_NAME = 'dev'
def DEV_NS = 'servicebc-ne-dev'

// Edit your application's context directory here
def CONTEXT_DIRECTORY = 'api'

def GIT_BRANCH_NAME = ("${env.JOB_BASE_NAME}".contains("master")) ? "master" : "develop"
def JENKINS_ICO = 'https://wiki.jenkins-ci.org/download/attachments/2916393/logo.png'
def OPENSHIFT_ICO = 'https://commons.wikimedia.org/wiki/File:OpenShift-LogoType.svg'

// define groovy functions
import groovy.json.JsonOutput

// Determine whether there were any changes the files within the project's context directory.
// return a string listing commit msgs occurred since last build
@NonCPS
String triggerBuild(String contextDirectory) {
    // Determine if code has changed within the source context directory.
    def changeLogSets = currentBuild.changeSets
    def filesChangeCnt = 0
    MAX_MSG_LEN = 512
    def changeString = ""
    for (int i = 0; i < changeLogSets.size(); i++) {
        def entries = changeLogSets[i].items
        for (int j = 0; j < entries.length; j++) {
            def entry = entries[j]
            //echo "${entry.commitId} by ${entry.author} on ${new Date(entry.timestamp)}: ${entry.msg}"
            def files = new ArrayList(entry.affectedFiles)

            for (int k = 0; k < files.size(); k++) {
                def file = files[k]
                def filePath = file.path
                //echo ">> ${file.path}"
                if (filePath.contains(contextDirectory)) {

                    filesChangeCnt = 1
                    truncated_msg = entry.msg.take(MAX_MSG_LEN)
                    changeString += " - ${truncated_msg} [${entry.author}]\n"
                    k = files.size()
                    j = entries.length
                }
            }
        }
    }
    if ( filesChangeCnt < 1 ) {
        echo('The changes do not require a build.')
        return ""
    }
    else {
        echo('The changes require a build.')
        return changeString
    }
}

// pipeline

// Note: openshiftVerifyDeploy requires policy to be added:
// oc policy add-role-to-user view system:serviceaccount:devex-platform-tools:jenkins -n devex-platform-dev
// oc policy add-role-to-user view system:serviceaccount:devex-platform-tools:jenkins -n devex-platform-test
// oc policy add-role-to-user view system:serviceaccount:devex-platform-tools:jenkins -n devex-platform-prod

// define job properties - keep 10 builds only
properties([
    [$class: 'BuildDiscarderProperty', strategy: [$class: 'LogRotator', artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '3'
        ]
    ]
])

def run_pipeline = true
if( triggerBuild(CONTEXT_DIRECTORY ) == "" ) 
    try {
        timeout(time: 1, unit: 'DAYS') {
            input message: "Run namex-api-pipeline?", id: "1234"
        }
    } catch (Exception e) {
        run_pipeline = false;
    }

}

if (!run_pipeline) {
    // The changeSets did not contain any changes within the project's context directory.
    // Clearly indicate there were no changes.
    stage('No Changes') {
        script {
            currentBuild.result = 'SUCCESS'
        }
    }
} else {
    //node/pod needs environment setup for testing
    node {
        stage('Checkout') {
            try {
                echo "checking out source"
                echo "Build: ${BUILD_ID}"
                checkout scm
                GIT_COMMIT_SHORT_HASH = sh (
                        script: """git describe --always""", returnStdout: true
                    ).trim()
                GIT_COMMIT_AUTHOR = sh (
                        script: """git show -s --pretty=%an""", returnStdout: true
                    ).trim()

            } catch (Exception e) {
                echo "error during checkout: ${e}"
                error('Aborted')
            }
        }//end stage
        stage('Build') {
            try {
                echo "Building..."
                openshiftBuild bldCfg: BUILDCFG_BASE, verbose: 'false', showBuildLogs: 'true'

                sleep 5

                // openshiftVerifyBuild bldCfg: BUILDCFG_NAME
                echo ">>> Get Image Hash"
                IMAGE_HASH = sh (
                    script: """oc get istag ${IMAGE_BASE_NAME}:latest -o template --template=\"{{.image.dockerImageReference}}\"|awk -F \":\" \'{print \$3}\'""",
                        returnStdout: true).trim()
                echo ">> IMAGE_HASH: ${IMAGE_HASH}"
                echo ">>>> Build Complete"

            } catch (Exception e) {
                echo "error during build: ${e}"
                error('Aborted')
            }
        }//end stage

        stage('Assemble Runtime') {
            try {
                echo "Building..."
                openshiftBuild bldCfg: BUILDCFG_RUNTIME, verbose: 'false', showBuildLogs: 'true'

                sleep 5

                // openshiftVerifyBuild bldCfg: BUILDCFG_NAME
                echo ">>> Get Image Hash"
                IMAGE_HASH = sh (
                    script: """oc get istag ${IMAGE_RUNTIME_NAME}:latest -o template --template=\"{{.image.dockerImageReference}}\"|awk -F \":\" \'{print \$3}\'""",
                        returnStdout: true).trim()
                echo ">> IMAGE_HASH: ${IMAGE_HASH}"
                echo ">>>> Build Complete"

            } catch (Exception e) {
                echo "error during assemble runtime: ${e}"
                error('Aborted')
            }
        }//end stage

        stage('Deploy DEV') {
            try {
                echo ">>> Tag ${IMAGE_HASH} with ${DEV_TAG_NAME}"
                openshiftTag destStream: IMAGE_RUNTIME_NAME, verbose: 'false', destTag: DEV_TAG_NAME, srcStream: IMAGE_RUNTIME_NAME, srcTag: "${IMAGE_HASH}"

                sleep 10

                openshiftVerifyDeployment depCfg: DEV_DEPLOYMENT_NAME, namespace: DEV_NS, replicaCount: 1, verbose: 'false', verifyReplicaCount: 'false'
                echo ">>>> Deployment Complete"

            } catch (Exception e) {
                echo "error during dev deploy: ${e}"
                error('Aborted')
            }
        }//end stage
    }//end node
}