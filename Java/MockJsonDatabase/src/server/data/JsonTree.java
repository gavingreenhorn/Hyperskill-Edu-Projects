package server.data;

import com.google.gson.Gson;
import com.google.gson.internal.LinkedTreeMap;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;
import java.util.*;

public class JsonTree {

    public static void main(String[] args) {
        String sampleJson = """
            {
                "person": {
                    "name": "John Doe",
                    "age": 30,
                    "employment": {
                        "company": "Tech Corp",
                        "salary": 75000,
                        "benefits": ["health", "dental"]
                    }
                }
            }
            """;

        System.out.println("=== Tree-based Approach ===");
        JsonTreeDatabase treeDb = new JsonTreeDatabase();
        treeDb.parseAndStore("doc1", sampleJson);

        // Access with tree approach
        System.out.println("Person name: " + treeDb.getValue("doc1", "person.name"));
        System.out.println("Salary: " + treeDb.getValue("doc1", "person.employment.salary"));

        System.out.println("\n=== LinkedTreeMap Approach ===");
        LinkedTreeMapDatabase linkedDb = new LinkedTreeMapDatabase();
        linkedDb.parseAndStore("doc1", sampleJson);

        // Access with LinkedTreeMap approach
        System.out.println("Person name: " + linkedDb.getValue("doc1", "person.name"));
        System.out.println("Salary: " + linkedDb.getValue("doc1", "person.employment.salary"));

        System.out.println("\n=== Performance and Memory Comparison ===");
        compareApproaches(sampleJson);
    }

    static void compareApproaches(String json) {
        // Memory and performance would be measured here in real scenarios
        System.out.println("Tree approach: More memory overhead, explicit type checking");
        System.out.println("LinkedTreeMap: Less memory, simpler traversal, type erasure");
    }
}

/**
 * THEORETICAL TREE-BASED APPROACH
 * Each node knows its type and children explicitly
 */
abstract class JsonNode {
    protected String key;

    public JsonNode(String key) {
        this.key = key;
    }

    public abstract boolean isLeaf();
    public abstract Object getValue();
    public String getKey() { return key; }
}

class JsonObjectNode extends JsonNode {
    private Map<String, JsonNode> children;

    public JsonObjectNode(String key) {
        super(key);
        this.children = new LinkedHashMap<>();
    }

    public void addChild(String key, JsonNode child) {
        children.put(key, child);
    }

    public JsonNode getChild(String key) {
        return children.get(key);
    }

    public Map<String, JsonNode> getChildren() {
        return children;
    }

    @Override
    public boolean isLeaf() { return false; }

    @Override
    public Object getValue() { return children; }
}

class JsonArrayNode extends JsonNode {
    private List<JsonNode> elements;

    public JsonArrayNode(String key) {
        super(key);
        this.elements = new ArrayList<>();
    }

    public void addElement(JsonNode element) {
        elements.add(element);
    }

    public JsonNode getElement(int index) {
        return index < elements.size() ? elements.get(index) : null;
    }

    public List<JsonNode> getElements() {
        return elements;
    }

    @Override
    public boolean isLeaf() { return false; }

    @Override
    public Object getValue() { return elements; }
}

class JsonLeafNode extends JsonNode {
    private Object value;

    public JsonLeafNode(String key, Object value) {
        super(key);
        this.value = value;
    }

    @Override
    public boolean isLeaf() { return true; }

    @Override
    public Object getValue() { return value; }

    public void setValue(Object value) { this.value = value; }
}

/**
 * Tree-based JSON Database Implementation
 */
class JsonTreeDatabase {
    private Map<String, JsonObjectNode> documents;
    private Gson gson = new Gson();

    public JsonTreeDatabase() {
        this.documents = new HashMap<>();
    }

    public void parseAndStore(String docId, String json) {
        // This is a simplified parser - in reality you'd need a full JSON parser
        // that builds the tree structure
        JsonObjectNode root = parseJsonToTree(json);
        documents.put(docId, root);
    }

    @SuppressWarnings("unchecked")
    private JsonObjectNode parseJsonToTree(String json) {
        // Using Gson to parse, then converting to tree structure
        // In pure tree approach, you'd write a custom parser
        LinkedTreeMap<String, Object> parsed = gson.fromJson(json,
            new TypeToken<LinkedTreeMap<String, Object>>(){}.getType());

        return convertToTree("root", parsed);
    }

    @SuppressWarnings("unchecked")
    private JsonObjectNode convertToTree(String key, LinkedTreeMap<String, Object> map) {
        JsonObjectNode node = new JsonObjectNode(key);

        for (Map.Entry<String, Object> entry : map.entrySet()) {
            String childKey = entry.getKey();
            Object value = entry.getValue();

            if (value instanceof LinkedTreeMap) {
                // Nested object
                JsonObjectNode childNode = convertToTree(childKey, (LinkedTreeMap<String, Object>) value);
                node.addChild(childKey, childNode);
            } else if (value instanceof List) {
                // Array
                JsonArrayNode arrayNode = new JsonArrayNode(childKey);
                List<?> list = (List<?>) value;
                for (int i = 0; i < list.size(); i++) {
                    Object element = list.get(i);
                    if (element instanceof LinkedTreeMap) {
                        arrayNode.addElement(convertToTree("[" + i + "]", (LinkedTreeMap<String, Object>) element));
                    } else {
                        arrayNode.addElement(new JsonLeafNode("[" + i + "]", element));
                    }
                }
                node.addChild(childKey, arrayNode);
            } else {
                // Leaf value
                node.addChild(childKey, new JsonLeafNode(childKey, value));
            }
        }

        return node;
    }

    public Object getValue(String docId, String path) {
        JsonObjectNode doc = documents.get(docId);
        if (doc == null) return null;

        String[] keys = path.split("\\.");
        JsonNode current = doc;

        for (String key : keys) {
            if (current instanceof JsonObjectNode) {
                current = ((JsonObjectNode) current).getChild(key);
                if (current == null) return null;
            } else {
                return null;
            }
        }

        return current.getValue();
    }

    // Tree approach allows for explicit type checking
    public boolean isLeafValue(String docId, String path) {
        JsonObjectNode doc = documents.get(docId);
        if (doc == null) return false;

        String[] keys = path.split("\\.");
        JsonNode current = doc;

        for (String key : keys) {
            if (current instanceof JsonObjectNode) {
                current = ((JsonObjectNode) current).getChild(key);
                if (current == null) return false;
            } else {
                return false;
            }
        }

        return current.isLeaf();
    }

    // Tree approach allows visiting all nodes with specific behavior
    public void visitAllNodes(String docId, JsonNodeVisitor visitor) {
        JsonObjectNode doc = documents.get(docId);
        if (doc != null) {
            visitNode(doc, visitor, "");
        }
    }

    private void visitNode(JsonNode node, JsonNodeVisitor visitor, String path) {
        visitor.visit(node, path);

        if (node instanceof JsonObjectNode) {
            JsonObjectNode objNode = (JsonObjectNode) node;
            for (Map.Entry<String, JsonNode> entry : objNode.getChildren().entrySet()) {
                String childPath = path.isEmpty() ? entry.getKey() : path + "." + entry.getKey();
                visitNode(entry.getValue(), visitor, childPath);
            }
        } else if (node instanceof JsonArrayNode) {
            JsonArrayNode arrayNode = (JsonArrayNode) node;
            for (int i = 0; i < arrayNode.getElements().size(); i++) {
                String childPath = path + "[" + i + "]";
                visitNode(arrayNode.getElements().get(i), visitor, childPath);
            }
        }
    }
}

interface JsonNodeVisitor {
    void visit(JsonNode node, String path);
}

/**
 * LINKEDTREEMAP APPROACH (Simplified)
 * Uses type erasure - everything is Object, determined at runtime
 */
class LinkedTreeMapDatabase {
    private Map<String, LinkedTreeMap<String, Object>> documents;
    private Gson gson = new Gson();
    private Type mapType = new TypeToken<LinkedTreeMap<String, Object>>(){}.getType();

    public LinkedTreeMapDatabase() {
        this.documents = new HashMap<>();
    }

    public void parseAndStore(String docId, String json) {
        LinkedTreeMap<String, Object> doc = gson.fromJson(json, mapType);
        documents.put(docId, doc);
    }

    @SuppressWarnings("unchecked")
    public Object getValue(String docId, String path) {
        LinkedTreeMap<String, Object> doc = documents.get(docId);
        if (doc == null) return null;

        String[] keys = path.split("\\.");
        Object current = doc;

        for (String key : keys) {
            if (current instanceof LinkedTreeMap) {
                current = ((LinkedTreeMap<String, Object>) current).get(key);
                if (current == null) return null;
            } else {
                return null;
            }
        }

        return current;
    }

    // LinkedTreeMap approach requires runtime type checking
    @SuppressWarnings("unchecked")
    public boolean isLeafValue(String docId, String path) {
        Object value = getValue(docId, path);
        return value != null &&
            !(value instanceof LinkedTreeMap) &&
            !(value instanceof List);
    }
}
