from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd


def bad_uris(source):
    sparql = SPARQLWrapper(source)
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    PREFIX obo: <http://purl.obolibrary.org/obo/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
    PREFIX edam:<http://edamontology.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT DISTINCT ?entity ?label WHERE {

        ?entity a owl:Class .
        ?entity rdfs:label ?label .
        FILTER NOT EXISTS { ?entity owl:deprecated true }

        FILTER NOT EXISTS {
            FILTER REGEX(str(?entity), "^http://edamontology.org/(data|topic|operation|format)_[0-9]{4}$")
       }
        FILTER ( ?entity != <http://www.geneontology.org/formats/oboInOwl#ObsoleteClass>)

    }
    ORDER BY ?entity
    
    """)   
    try: 
        ret = sparql.queryAndConvert()
        results = []
        for r in ret["results"]["bindings"]:
            results.append(r)
        uris = []
        for result in results: 
            uris.append(result)
        df = pd.DataFrame({"uri": uris})
        pd.set_option('display.max_rows', None)
        return df

    except: 
        print("Oh Noes!")


def classes_with_definitions(source):
    sparql = SPARQLWrapper(source)
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    PREFIX obo-term: <http://purl.obolibrary.org/obo/>
    SELECT ?s ?label ?definition ?author
    FROM <http://purl.obolibrary.org/obo/merged/VO>
    {
    ?s a owl:Class .
    ?s rdfs:label ?label .
    ?s obo-term:IAO_0000115 ?definition .
    ?s obo-term:IAO_0000117 ?author .
    }
    """)
    try: 
        ret = sparql.queryAndConvert()
        results = []
        for r in ret["results"]["bindings"]:
            results.append(r)
        s = []
        label = []
        definition = []
        author = []
        for result in results:
            s.append(result["s"]["value"])
            label.append(result["label"]["value"])
            definition.append(result["definition"]["value"])
            author.append(result["author"]["value"])
        df = pd.DataFrame({"s": s, "label": label, "definition":definition, "author":author})
        pd.set_option('display.max_rows', None)
            
        return df 
    except:
        print("oh noes!")

def class_counts(source):
    sparql = SPARQLWrapper(source)
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    SELECT count(?s) as ?VO_class_count
    FROM <http://purl.obolibrary.org/obo/merged/VO>
    WHERE
    {
    ?s a owl:Class .
    ?s rdfs:label ?label .

    FILTER regex( ?s, "VO_" )
    }
    """)
    try: 
        ret = sparql.queryAndConvert()
        results = []
        for r in ret["results"]["bindings"]:
            results.append(r)
        classes = []
        for result in results:
            classes.append(result['VO_class_count']['value'])
        df = pd.DataFrame({"VO_class_count": classes})
        pd.set_option('display.max_rows', None)

        return df
    except: 
        print("Oh Noes!")

def object_property_counts(source):
    sparql = SPARQLWrapper(source)
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    SELECT count(?s) as ?VO_object_property_count
    FROM <http://purl.obolibrary.org/obo/merged/VO>
    WHERE
    {
    ?s a owl:ObjectProperty .
    ?s rdfs:label ?label .

    FILTER regex( ?s, "VO_" )
    }
    """)
    try: 
        ret = sparql.queryAndConvert()
        results = []
        for r in ret["results"]["bindings"]:
            results.append(r)
        classes = []
        for result in results:
            classes.append(result['VO_object_property_count']['value'])
        df = pd.DataFrame({"VO_object_property_count": classes})
        pd.set_option('display.max_rows', None)

        return df
    except: 
        print("Oh Noes!")


def annotation_property_counts(source):
    sparql = SPARQLWrapper(source)
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    SELECT count(?s) as ?VO_annotation_property_count
    FROM <http://purl.obolibrary.org/obo/merged/VO>
    WHERE
    {
    ?s a owl:AnnotationProperty .
    ?s rdfs:label ?label .

    FILTER regex( ?s, "VO_" )
    }
    """)
    try: 
        ret = sparql.queryAndConvert()
        results = []
        for r in ret["results"]["bindings"]:
            results.append(r)
        classes = []
        for result in results:
            classes.append(result['VO_annotation_property_count']['value'])
        df = pd.DataFrame({"VO_annotation_property_count": classes})
        pd.set_option('display.max_rows', None)

        return df
    except: 
        print("Oh Noes!")

def datatype_property_counts(source):
    sparql = SPARQLWrapper(source)
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    SELECT count(?s) as ?VO_datatype_property_count
    FROM <http://purl.obolibrary.org/obo/merged/VO>
    WHERE
    {
    ?s a owl:DatatypeProperty .
    ?s rdfs:label ?label .

    FILTER regex( ?s, "VO_" )
    }
    """)
    try: 
        ret = sparql.queryAndConvert()
        results = []
        for r in ret["results"]["bindings"]:
            results.append(r)
        classes = []
        for result in results:
            classes.append(result['VO_datatype_property_count']['value'])
        df = pd.DataFrame({"VO_datatype_property_count": classes})
        pd.set_option('display.max_rows', None)

        return df
    except: 
        print("Oh Noes!")


#Function to find all class containing graphs (JSON Output)
def class_containing_graphs(source):
    sparql = SPARQLWrapper(source)
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix owl: <http://www.w3.org/2002/07/owl#>
    
    SELECT distinct ?graph_uri
    WHERE {
    GRAPH ?graph_uri
    { ?s rdf:type owl:Class }
    }
    LIMIT 10
    """)
    try: 
        ret = sparql.queryAndConvert()
        results = []
        for r in ret["results"]["bindings"]:
            results.append(r)
        graph_uris = []
        for result in results:
            graph_uris.append(result['graph_uri']['value'])
        df = pd.DataFrame({"graph_uri": graph_uris})
        pd.set_option('display.max_rows', None)

        return df
    except: 
        print("Oh Noes!")

def find_all_subclasses(source):
    sparql = SPARQLWrapper(source)
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    PREFIX obo-term: <http://purl.obolibrary.org/obo/>
    SELECT DISTINCT ?x ?label
    WHERE
    {
    ?x rdfs:subClassOf obo-term:OAE_0000001.
    ?x rdfs:label  ?label.
    }
    """)
    try: 
        ret = sparql.queryAndConvert()
        results = []
        for r in ret["results"]["bindings"]:
            results.append(r)
        x = []
        label = []
        for result in results: 
            label.append(result["label"]["value"])
            x.append(result["x"]["value"])
        df = pd.DataFrame({"label": label, "x": x})
        pd.set_option('display.max_rows', None)
        return df
    except: 
        print("Oh Noes!")

def general_annotations(source):
    sparql = SPARQLWrapper(source)
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT DISTINCT ?p ?o 
    FROM <http://purl.obolibrary.org/obo/merged/OAE>
    WHERE
    {
    ?s a owl:Ontology.
    ?s ?p ?o .
    }
    """)
    try: 
        ret = sparql.queryAndConvert()
        results = []
        for r in ret["results"]["bindings"]:
            results.append(r)
        p = []
        o = []
        for result in results:
            p.append(result["p"]["value"])
            o.append(result["o"]["value"])
        df = pd.DataFrame({"p": p, "o":o})
        pd.set_option('display.max_rows', None)
            
        return df 
    except:
        print("oh noes!")

def get_uris(source):
    sparql = SPARQLWrapper(source)
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    PREFIX obo: <http://purl.obolibrary.org/obo/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
    PREFIX edam:<http://edamontology.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT DISTINCT ?entity ?label WHERE {

        ?entity a owl:Class .
        OPTIONAL  {?entity rdfs:label ?label .}

    }
    ORDER BY ?entity
    LIMIT 200
    """)
    try: 
        ret = sparql.queryAndConvert()
        results = []
        for r in ret["results"]["bindings"]:
            results.append(r)
        label = []
        entity = []
        for result in results:
            label.append(result["label"]["value"])
            entity.append(result["entity"]["value"])
        df = pd.DataFrame({"label": label, "entity": entity})
        pd.set_option('display.max_rows', None)
        
        return df 
    except:
        print("oh noes!")

#Function to find all missing wikis (JSON Output)
def missing_wikis(source):
    sparql = SPARQLWrapper(source)
    sparql.setReturnFormat(JSON)
    sparql.setQuery("""
    PREFIX obo: <http://purl.obolibrary.org/obo/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
    PREFIX edam:<http://edamontology.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT DISTINCT ?entity ?label ?seealso WHERE {
        ?entity rdfs:subClassOf+ <http://edamontology.org/topic_0003> .
        ?entity rdfs:label ?label .

        FILTER NOT EXISTS {
            ?entity rdfs:seeAlso ?seealso .
            FILTER (regex(str(?seealso), "wikipedia", "i")) .
        }
    }
    """)
    try: 
        ret = sparql.queryAndConvert()
        results = []
        for r in ret["results"]["bindings"]:
            results.append(r)
        entity = []
        label = []
        for result in results: 
            entity.append(result["entity"]['value'])
            label.append(result["label"]["value"])

        df = pd.DataFrame({"entity": entity, "label": label})
        pd.set_option('display.max_rows', None)

        return df
    except: 
        print("Oh Noes!")