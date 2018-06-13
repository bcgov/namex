from urllib import request, parse
import json

class SolrQueries:
    queries ={
        'similar': '/solr/{core}/select?q=id:{name}&wt=json',
        'conflicts': '/solr/possible.conflicts/select?indent=on&start={start}&rows={rows}&defType=dismax&fl=source,id,name,score&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&hl=on&indent=on&pf=name%5E100&q=name:{name}&qf=name&wt=json'
    }

    @classmethod
    def get_name_conflicts(cls, base_url, name, start=0, rows=10):

        query = base_url + SolrQueries.queries['conflicts'].format(
            start=start,
            rows=rows,
            name=parse.quote(name)
        )
        connection = request.urlopen(query)
        print (connection)
        return json.load(connection)

