from ..parser.parser import xmlToJson


def manageFiles(files, nodes, edges, node_set, edge_set):
    """ Leer todos los archivos y manejar la creación de
    sus nodos y relaciones.

    Parameters
    ----------
    files: list
        lista con todos los archivos XML
    nodes: list
        lista con todos los nodos de la arquitectura
    edges: list
        lista con todas las aristas de la arquitectura
    node_set: set
        set para mantener constancia de los nodos ya creados
    edge_set
        set pata mantener constancia de las aristas ya creadas
    """
    for file in files:
        file_json = xmlToJson(file)
        handleGraphBuild(file_json, nodes, edges, node_set, edge_set)


def handleGraphBuild(json, nodes, edges, node_set, edge_set):
    """ Inicialización de los nodos y aristas de un archivo

    Parameters
    ----------
    json: dict
        diccionario de archivo XML convertido a json
    nodes: list
        lista con todos los nodos de la arquitectura
    edges: list
        lista con todas las aristas de la arquitectura
    node_set: set
        set para mantener constancia de los nodos ya creados
    edge_set
        set pata mantener constancia de las aristas ya creadas
    """
    base = json['doxygen']['compounddef']
    if(base['compoundname'] == 'README.md'):
        return
    node = createNode(base, node_set)
    if node is not None:
        nodes.append(node)
        node_set.add(node['data']['id'])
    handleEdgeCreation(base, edges, nodes, node_set, edge_set)


def getClassId(base):
    """ Obtener el ID de la clase del archivo

    que está siendo leído
    Parameters
    ----------
    base: dict
        diccionario con información del nodo

    Returns
    -------
    str
        id del nodo
    """
    class_name = base['compoundname']
    file_name = class_name.split('.')
    node_id = file_name[0]
    return node_id


def createNode(base, node_set):
    """ Creación del objeto nodo
    Parameters
    ----------
    base: dict
        diccionario con información del nodo
    node_set: set
        set para mantener constancia de los nodos ya creados

    Returns
    -------
    dict
        diccionario con el objeto nodo creado
    """
    class_id = getClassId(base)
    if class_id in node_set:
        return None
    node = {
        "data": {
            "id": class_id,
            "name": class_id
        }
    }
    return node


def handleEdgeCreation(base, edges, nodes, node_set, edge_set):
    """ Manejar la creación de las aristas de un archivo.

    Parameters
    ----------
    base: dict
        diccionario con información del nodo
    nodes: list
        lista con todos los nodos de la arquitectura
    edges: list
        lista con todas las aristas de la arquitectura
    node_set: set
        set para mantener constancia de los nodos ya creados
    edge_set
        set pata mantener constancia de las aristas ya creadas
    """
    codeline = base['programlisting']['codeline']
    for line in codeline:
        highlight = line['highlight']
        if highlight:
            if type(highlight) is list:
                L = len(highlight)
                relation = highlight[L-2]['#text']
                if relation is None:
                    continue
                if relation == 'implements':
                    class_name = getClassName(highlight, L)
                    all_classes = handleClassDivision(class_name)
                    for c in all_classes:
                        if c == "":
                            continue
                        createEdge(base, c, relation,
                                   edges, nodes, node_set, edge_set)
                elif relation == 'extends':
                    class_name = getClassName(highlight, L)
                    if 'implements' not in class_name:
                        all_classes = handleClassDivision(class_name)
                        for c in all_classes:
                            if c == "":
                                continue
                            createEdge(base, c,
                                       relation, edges, nodes, node_set, edge_set)
                    else:
                        classes = class_name.split('implements')
                        all_extends = handleClassDivision(classes[0])
                        all_implements = ''
                        if classes[len(classes)-1] == '':
                            temp_implements = highlight[L-1]['ref']['#text']
                            all_implements = handleClassDivision(
                                temp_implements)
                        else:
                            all_implements = handleClassDivision(classes[1])
                        for c in all_extends:
                            if c == "":
                                continue
                            createEdge(base, c,
                                       relation, edges, nodes, node_set, edge_set)
                        for c in all_implements:
                            if c == "":
                                continue
                            createEdge(base, c,
                                       "implements", edges, nodes, node_set, edge_set)
            else:
                if '#text' in highlight:
                    if checkUse(highlight['#text']):
                        class_name = ''
                        relation = 'use'
                        if highlight['#text'] == 'use;':
                            class_name = getUseClassName(
                                highlight['ref']['#text'])
                        else:
                            class_name = getUseClassName(highlight['#text'])

                        createEdge(base, class_name, relation,
                                   edges, nodes, node_set, edge_set)


def checkUse(base):
    """ Comprobar si la clase está siendo
    utilizada
    Parameters
    ----------
    base: string
        string con la información de la clase
    """
    if len(base) < 3:
        return False
    temp = base[0:3]
    if temp == 'use':
        return True
    else:
        return False


def getUseClassName(base):
    """ Obtener el nombre de la clase de
    tipo use de un nodo

    Parameters
    ----------
    base: string
        string con la información de la clase

    Returns
    -------
    str
        nombre de la clase  
    """
    class_name = ""
    for c in base[::-1]:
        if c == "\\":
            break
        class_name = c + class_name
    if class_name[len(class_name)-1] == ';':
        class_name = class_name[0:len(class_name)-1]
    if class_name[0:3] == 'use':
        class_name = class_name[3:len(class_name)]
    return class_name


def getClassName(base, L):
    """ Obtener el nombre de la clase de un nodo

    Parameters
    ----------
    base: list
        lista con la información de la clase
    L: int
        tamaño de la lista

    Returns
    -------
    str
        nombre de la clase
    """
    try:
        class_name = base[L-1]['#text']
        return class_name
    except:
        class_name = base[L-1]['ref']['#text']
        return class_name


def createEdge(base, class_name, relation, edges, nodes, node_set, edge_set):
    """ Creación del objeto arista.

    Parameters
    ----------
    base: dict
        diccionario con información del nodo
    class_name: str
        nombre de la clase
    relation: str
        tipo de relación
    edges: list
        lista con todas las aristas de la arquitectura
    nodes: list
        lista con todos los nodos de la arquitectura
    node_set: set
        set para mantener constancia de los nodos ya creados
    edge_set
        set pata mantener constancia de las aristas ya creadas
    """
    source_class_name = getClassId(base)
    target_class_name = class_name
    if target_class_name not in node_set:
        createNode2(target_class_name, nodes, node_set)
    data = {
        "id": source_class_name + "-" + target_class_name,
        "name": source_class_name + "-" + target_class_name,
        "source": source_class_name,
        "target": target_class_name

    }
    scratch = {
        "relation": relation
    }
    if data['id'] not in edge_set:
        edges.append({"data": data, "scratch": scratch})
        edge_set.add(data['id'])
    else:
        if scratch['relation'] != 'use':
            for i in range(len(edges)):
                if edges[i]['data'] == data:
                    edges[i]['scratch'] = scratch
                    break


def createNode2(class_name, nodes, node_set):
    """ Creación del objeto nodo e inclusión en el 
    arreglo y set de nodos

    Parameters
    ----------
    class_name: str
        nombre de la clase
    nodes: list
        lista con todos los nodos de la arquitectura
    node_set: set
        set para mantener constancia de los nodos ya creados

    Returns
    -------
    dict
        diccionario con el objeto nodo creado
    """
    node = {
        "data": {
            "id": class_name,
            "name": class_name
        }
    }
    node_set.add(class_name)
    nodes.append(node)
    return node


def handleClassDivision(class_name):
    """ Obtención de un arreglo con todas las clases
    relacionadas con un nodo

    Parameters
    ----------
    class_name: str
        nombre de la clase

    Returns
    -------
    list
        lista con todas las clases
    """
    if "\\" in class_name:
        return class_name.split("\\")
    return class_name.split(",")


def getNodeIds(nodes):
    """ Obtención del set con todos los nodos de
    una arquitectura.

    Parameters
    ----------
    nodes: list
        lista con todos los nodos de la arquitectura

    Returns
    -------
    set
        set con todos los nodos de la arquitectura sin repetición
    """
    node_ids = set()
    for node in nodes:
        node_ids.add(node['data']['id'])
    return node_ids


def getEdgeIds(edges):
    """" Obtención del set con todas las aristas
    de una arquitectura.

    Parameters
    ----------
    edges: list
        lista con todas las aristas de la arquitectura

    Returns
    -------
    set
        set con todas las aristas de la arquitectura sin repetición
    """
    edge_ids = set()
    for edge in edges:
        edge_ids.add(edge['data']['id'])
    return edge_ids
