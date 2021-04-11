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
                                v-model="tags"
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

export default {
  name: "GraphBrowser",
  components: {
    D3Network
  },
  data: function () {
    return {
        tags: ["Ciao", "Lorem"],
        graph: {
            nodes: [
                { id: 1, name: 'my awesome node 1'},
                { id: 2, name: 'my node 2'},
                { id: 3, name:'orange node', _color: 'orange' },
                { id: 4, _color: '#4466ff'},
                { id: 5 },
                { id: 6 },
                { id: 7 },
                { id: 8 },
                { id: 9 }
            ],
            links: [
                { sid: 1, tid: 2, _color: "#000000" },
                { sid: 2, tid: 8, _color: "#000000" },
                { sid: 3, tid: 4,  _color: "#000000", name:'custom link'},
                { sid: 4, tid: 5, _color: "#000000" },
                { sid: 5, tid: 6, _color: "#000000" },
                { sid: 7, tid: 8, _color: "#000000" },
                { sid: 5, tid: 8, _color: "#000000" },
                { sid: 3, tid: 8, _color: "#000000" },
                { sid: 7, tid: 9, _color: "#000000" }
            ]
        },
        graphOptions: {
            nodeSize: 30,
            nodeLabels: true,
            linkLabels:true,
            force: 3000
        }
    }
  },
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