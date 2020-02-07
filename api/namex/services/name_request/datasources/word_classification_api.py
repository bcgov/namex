class WordClassificationApi:
    @staticmethod
    def get_word_classification(word):
        # df = pd.read_sql_query('select word,classification,counter from word_classification where word=' + "'" + \
        #                       word + "'", cnx)
        # return df
        pass

    @staticmethod
    def update_word_classification(word, classification):
        # stmt = word_classification.update(). \
        #    where(and_(word_classification.c.word == word,
        #               word_classification.c.classification == classification)). \
        #    values(counter=word_classification.c.counter + 1)
        # result = cnx.execute(stmt)

        # return result
        pass

    # Query database for synonyms, substitutions and designations
    df_syn = pd.read_sql_query('SELECT synonyms_text,stems_text FROM synonym where mode=' + "'" + MODE_SYNS + "'" + ';',
                               cnx_syns)
    df_sub = pd.read_sql_query(
        'SELECT synonyms_text,stems_text FROM synonym where mode=' + "'" + MODE_SUBS + "'" + ' AND synonyms_text like ' + "'1st%%" + "'" + ';',
        cnx_syns)
    df_sub = pd.read_sql_query('SELECT synonyms_text,stems_text FROM synonym where mode=' + "'" + MODE_SUBS + "'" + ';',
                               cnx_syns)
    df_stopWords = pd.read_sql_query(
        'SELECT synonyms_text FROM synonym where mode=' + "'" + MODE_STOP + "'" + 'AND category=' + "'" + stop_w + "'" + ';',
        cnx_syns)
    df_dsg_end = pd.read_sql_query(
        'SELECT synonyms_text FROM synonym where mode=' + "'" + MODE_STOP + "'" + ' AND category=' + "'" + dsg_end + "'" + ';',
        cnx_syns)
    df_dsg_any = pd.read_sql_query(
        'SELECT synonyms_text FROM synonym where mode=' + "'" + MODE_STOP + "'" + ' AND category=' + "'" + dsg_any + "'" + ';',
        cnx_syns)

    # df_solr_one=pd.read_sql_query("SELECT id,name FROM solr_dataimport_conflicts_vw WHERE jurisdiction='BC' AND name='REAL EARTH 2 (HOLDINGS) LIMITED';", cnx)
    df_solr = pd.read_sql_query("select r.nr_num AS ID, n.name, r.submitted_date AS start_date,'BC' AS jurisdiction " \
                                "from requests r, names n " \
                                "where r.id = n.nr_id and " \
                                "r.state_cd IN ('APPROVED','CONDITIONAL') and " \
                                "r.request_type_cd IN ('PA','CR','CP','FI','SO', 'UL','CUL','CCR','CFI','CCP','CSO','CCC','CC') and " \
                                "n.state IN ('APPROVED','CONDITION');", cnx)
