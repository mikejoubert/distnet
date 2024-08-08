To render the DAG network in a React application using the provided JSON structure, we can utilize a graph visualization library such as `react-d3-graph`. This library allows us to create and render a directed graph (DAG) easily.

Here's a step-by-step guide to create the React routine:

1. **Install necessary packages:**
   - `react-d3-graph` for graph visualization.
   - `react` and `react-dom` if not already installed.

   Run the following command:
   ```sh
   npm install react react-dom react-d3-graph
   ```

2. **Set up the React application:**

   Create a new React component called `NetworkGraph.js`:

   ```jsx
   import React from "react";
   import { Graph } from "react-d3-graph";

   // Read the JSON data (assuming it is in the same directory)
   import networkData from "./network_data.json";

   const NetworkGraph = () => {
       const nodes = [];
       const links = [];

       // Prepare nodes and links from the JSON data
       networkData.forEach((board) => {
           nodes.push({ id: board.node_id, label: board.name });

           board.circuits.forEach((circuit) => {
               if (circuit.child_node_id !== null) {
                   links.push({ source: board.node_id, target: circuit.child_node_id, label: `Circuit ${circuit.circuit_number}` });
               }
           });
       });

       const data = {
           nodes,
           links,
       };

       const config = {
           nodeHighlightBehavior: true,
           node: {
               color: "lightgreen",
               size: 120,
               highlightStrokeColor: "blue",
           },
           link: {
               highlightColor: "lightblue",
           },
           directed: true,
       };

       return <Graph id="network-graph" data={data} config={config} />;
   };

   export default NetworkGraph;
   ```

3. **Use the `NetworkGraph` component in your application:**

   Modify your `App.js` to include the `NetworkGraph` component:

   ```jsx
   import React from "react";
   import NetworkGraph from "./NetworkGraph";

   const App = () => {
       return (
           <div>
               <h1>Electrical Network DAG</h1>
               <NetworkGraph />
           </div>
       );
   };

   export default App;
   ```

4. **Ensure your JSON data is correctly imported:**

   Make sure your `network_data.json` file is in the same directory as `NetworkGraph.js` or adjust the import path accordingly.

5. **Run your React application:**

   Start your React application using:
   ```sh
   npm start
   ```

### Explanation:
- **Data Preparation:**
  - Nodes are created for each board using the `node_id` as the identifier and the `name` as the label.
  - Links are created between nodes using the `circuit_number` to `child_node_id` relationship.

- **Graph Configuration:**
  - `nodeHighlightBehavior`, `node`, and `link` are configured to provide better visualization with highlighting features.
  - `directed: true` ensures the graph is treated as a directed graph.

With this setup, the React application will render the DAG network based on the JSON data structure provided. Each node represents a board, and each link represents a circuit connecting to a child board.