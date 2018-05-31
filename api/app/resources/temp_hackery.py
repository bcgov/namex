
class hackery():

    conflict_names = {  "responseHeader":{
    "status":0,
    "QTime":18,
    "params":{
      "q":"name:  THIRD  CONSENT  EXPIRY  TEST  A  INC.",
      "defType":"dismax",
      "hl.simple.post":"</b>",
      "hl":"on",
      "indent":"on",
      "qf":"name",
      "fl":"nr_num, name, choice_number, request_type_cd, name_state_type_cd, score, name_instance_id, request_id,",
      "pf":"name^100",
      "hl.fl":"name",
      "wt":"json",
      "hl.simple.pre":"<b>"}},
  "response":{"numFound":2991,"start":0,"maxScore":18.873959,"docs":[
      {
        "nr_num":"NR 0369789",
        "name_instance_id":"575771",
        "request_id":437287,
        "choice_number":1,
        "request_type_cd":"CR",
        "name_state_type_cd":"R",
        "name":"3RD CONSENT EXPIRY TEST A INC.",
        "score":18.873959},
      {
        "nr_num":"NR 0369789",
        "name_instance_id":"575770",
        "request_id":437287,
        "choice_number":2,
        "request_type_cd":"CR",
        "name_state_type_cd":"R",
        "name":"3RD CONSENT EXPIRY TEST B INC.",
        "score":15.688514},
      {
        "nr_num":"NR 0369789",
        "name_instance_id":"575772",
        "request_id":437287,
        "choice_number":3,
        "request_type_cd":"CR",
        "name_state_type_cd":"C",
        "name":"3RD CONSENT EXPIRY TEST C INC.",
        "score":15.688514},
      {
        "nr_num":"NR 4612135",
        "name_instance_id":"575762",
        "request_id":437284,
        "choice_number":1,
        "request_type_cd":"CR",
        "name_state_type_cd":"R",
        "name":"3RD EXPIRY EMAIL TEST A LTD.",
        "score":14.665398},
      {
        "nr_num":"NR 7860651",
        "name_instance_id":"575768",
        "request_id":437286,
        "choice_number":1,
        "request_type_cd":"CR",
        "name_state_type_cd":"R",
        "name":"2ND CONSENT EXPIRY TEST A INC.",
        "score":13.21427},
      {
        "nr_num":"NR 4612135",
        "name_instance_id":"575763",
        "request_id":437284,
        "choice_number":2,
        "request_type_cd":"CR",
        "name_state_type_cd":"R",
        "name":"3RD EXPIRY EMAIL TEST B LTD.",
        "score":11.479952},
      {
        "nr_num":"NR 4612135",
        "name_instance_id":"575764",
        "request_id":437284,
        "choice_number":3,
        "request_type_cd":"CR",
        "name_state_type_cd":"A",
        "name":"3RD EXPIRY EMAIL TEST C LTD.",
        "score":11.479952},
      {
        "nr_num":"NR 4002458",
        "name_instance_id":"575766",
        "request_id":437285,
        "choice_number":1,
        "request_type_cd":"CR",
        "name_state_type_cd":"C",
        "name":"CONSENT EXPIRY TESTING 1 INC.",
        "score":11.4086},
      {
        "nr_num":"NR 7860651",
        "name_instance_id":"575769",
        "request_id":437286,
        "choice_number":2,
        "request_type_cd":"CR",
        "name_state_type_cd":"A",
        "name":"2ND CONSENT EXPIRY TEST B INC.",
        "score":10.028825},
      {
        "nr_num":"NR 4105427",
        "name_instance_id":"574748",
        "request_id":436867,
        "choice_number":1,
        "request_type_cd":"SO",
        "name_state_type_cd":"R",
        "name":"A STAFF THIRD SOCIETY INCORPORATION",
        "score":9.830394}]
  },
  "highlighting":{
    "575771":{
      "name":["<b>3RD</b> <b>CONSENT</b> <b>EXPIRY</b> <b>TEST</b> <b>A</b> INC."]},
    "575770":{
      "name":["<b>3RD</b> <b>CONSENT</b> <b>EXPIRY</b> <b>TEST</b> B INC."]},
    "575772":{
      "name":["<b>3RD</b> <b>CONSENT</b> <b>EXPIRY</b> <b>TEST</b> C INC."]},
    "575762":{
      "name":["<b>3RD</b> <b>EXPIRY</b> EMAIL <b>TEST</b> <b>A</b> LTD."]},
    "575768":{
      "name":["2ND <b>CONSENT</b> <b>EXPIRY</b> <b>TEST</b> <b>A</b> INC."]},
    "575763":{
      "name":["<b>3RD</b> <b>EXPIRY</b> EMAIL <b>TEST</b> B LTD."]},
    "575764":{
      "name":["<b>3RD</b> <b>EXPIRY</b> EMAIL <b>TEST</b> C LTD."]},
    "575766":{
      "name":["<b>CONSENT</b> <b>EXPIRY</b> <b>TESTING</b> 1 INC."]},
    "575769":{
      "name":["2ND <b>CONSENT</b> <b>EXPIRY</b> <b>TEST</b> B INC."]},
    "574748":{
      "name":["<b>A</b> STAFF <b>THIRD</b> SOCIETY INCORPORATION"]}}}


    registry = {
        "responseHeader": {
            "status": 0,
            "QTime": 14,
            "params": {
                "q": "name:  THIRD  CONSENT  EXPIRY  TEST  A  INC.",
                "defType": "dismax",
                "hl.simple.post": "</b>",
                "hl": "on",
                "indent": "on",
                "qf": "name",
                "fl": "corp_num, name, state_typ_cd,score",
                "pf": "name^100",
                "hl.fl": "name",
                "wt": "json",
                "hl.simple.pre": "<b>"}},
        "response": {"numFound": 18223, "start": 0, "maxScore": 16.591677, "docs": [
            {
                "state_typ_cd": "ACT",
                "corp_num": "LLC0000405",
                "name": "MIKE'S THIRD TEST LLC",
                "score": 16.591677},
            {
                "state_typ_cd": "ACT",
                "corp_num": "LLC0000406",
                "name": "LINDA'S THIRD TEST LLC",
                "score": 16.591677},
            {
                "state_typ_cd": "ACT",
                "corp_num": "A0053181",
                "name": "EXPIRY CORPORATION",
                "score": 16.519533},
            {
                "state_typ_cd": "ACT",
                "corp_num": "FM1002871",
                "name": "TESTING EXPIRY DATE",
                "score": 16.499966},
            {
                "state_typ_cd": "ACT",
                "corp_num": "0874434",
                "name": "EXPIRY TESTS AB & SK LIMITED",
                "score": 16.499966},
            {
                "state_typ_cd": "D1F",
                "corp_num": "A0054068",
                "name": "REINSTATEMENT NR EXPIRY TESTING INC.",
                "score": 16.499966},
            {
                "state_typ_cd": "ACT",
                "corp_num": "FM1000204",
                "name": "TEST OF CONSENT AGAIN",
                "score": 16.226864},
            {
                "state_typ_cd": "ACT",
                "corp_num": "FM1000205",
                "name": "TEST OF CONSENT AGAIN",
                "score": 16.226864},
            {
                "state_typ_cd": "ACT",
                "corp_num": "FM1004759",
                "name": "TEST PROP WITH CONSENT",
                "score": 16.226864},
            {
                "state_typ_cd": "ACT",
                "corp_num": "FM1000206",
                "name": "TEST OF CONSENT AGAIN",
                "score": 16.226864}]
                     },
        "highlighting": {
            "LLC0000405": {
                "name": ["MIKE'S <b>THIRD</b> <b>TEST</b> LLC"]},
            "LLC0000406": {
                "name": ["LINDA'S <b>THIRD</b> <b>TEST</b> LLC"]},
            "A0053181": {
                "name": ["<b>EXPIRY</b> CORPORATION"]},
            "FM1002871": {
                "name": ["<b>TESTING</b> <b>EXPIRY</b> DATE"]},
            "0874434": {
                "name": ["<b>EXPIRY</b> <b>TESTS</b> AB & SK LIMITED"]},
            "A0054068": {
                "name": ["REINSTATEMENT NR <b>EXPIRY</b> <b>TESTING</b> INC."]},
            "FM1000204": {
                "name": ["<b>TEST</b> OF <b>CONSENT</b> AGAIN"]},
            "FM1000205": {
                "name": ["<b>TEST</b> OF <b>CONSENT</b> AGAIN"]},
            "FM1004759": {
                "name": ["<b>TEST</b> PROP WITH <b>CONSENT</b>"]},
            "FM1000206": {
                "name": ["<b>TEST</b> OF <b>CONSENT</b> AGAIN"]}}}
