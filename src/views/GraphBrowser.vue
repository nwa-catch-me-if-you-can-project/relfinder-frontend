<template>
    <div class="container is-fluid app-container">
        <div class="columns">
            <div class="column is-3 app-sidebar-col">
                <nav class="panel app-sidebar">
                    <p class="panel-heading">
                        UM-IDS RelFinder
                    </p>
                    <div class="panel-block">
                        <b-field label="Select Entities">
                            <b-taginput
                                v-model="this.classes"
                                ellipsis
                                icon="label"
                                placeholder="Add a tag"
                                aria-close-label="Delete this tag">
                            </b-taginput>
                        </b-field>
                    </div>

                    <div class="panel-block">
                        <b-button type="is-primary refresh-btn">Refresh Graph</b-button>
                    </div>
                </nav>
            </div>
            <div class="column rel-network-col">
                <d3-network
                    class="rel-network"
                    ref="relationship-network"
                    :net-nodes="this.graph.nodes"
                    :net-links="this.graph.links"
                    :options="graphOptions" />
            </div>
        </div>
    </div>
</template>

<script>

import D3Network from 'vue-d3-network'
import mockGraph from '@/../graph/demo-graph.json'

export default {
  name: "GraphBrowser",
  components: {
    D3Network
  },
  data: function () {
    return {
        classes: [],
        graph: {
            nodes: [],
            links: []
        },
        graphOptions: {
            nodeSize: 30,
            nodeLabels: true,
            linkLabels:true,
            force: 4500
        }
    }
  },
  mounted: function () {
    this.classesData = {};
    this.classes = mockGraph.classes.map(x => x.class);

    mockGraph.classes.forEach(clsObject => (this.classesData[clsObject.class] = { color: clsObject.color }));

    this.graph.nodes = mockGraph.nodes;
    this.graph.links = mockGraph.edges;

    this.graph.nodes.forEach(n => (
        n._color = this.classesData[n.class].color
    ));
  }
};

</script>

<style scoped>

.app-container {
    padding-left: 0px;
    padding-right: 0px;
}

.app-sidebar {
    height: 100vh;
}

.rel-network {
    height: 100vh;
}

.rel-network-col {
    padding-left: 0px;
    padding-bottom: 0px;
}

.app-sidebar-col {
    padding-bottom: 0px;
    padding-right: 0px;
}

.entities-block {
    background-color: #ededed;
}

.refresh-btn {
    width: 100%;
}

</style>