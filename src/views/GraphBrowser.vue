<template>
    <div class="container is-fluid app-container">
        <div class="columns">
            <div class="column is-3 app-sidebar-col">
                <nav class="panel app-sidebar">
                    <p class="panel-heading">
                        UM-IDS RelFinder
                    </p>
                    <div class="panel-block">
                        <b-field label="Select Entities" class="entities-tag-input">
                            <b-taginput
                                v-model="selectedClasses"
                                :data="filteredClasses"
                                autocomplete
                                icon="label"
                                :open-on-focus="true"
                                placeholder="Add a tag"
                                aria-close-label="Delete this tag"
                                @typing="getFilteredTags"
                                @add="tagListEdited"
                                @remove="tagListEdited">
                            </b-taginput>
                        </b-field>
                    </div>

                    <div class="panel-block">
                        <div class="container is-fluid buttons-container">
                            <div class="columns">
                                <div class="column">
                                    <b-button
                                        @click="refreshGraph"
                                        type="is-primary refresh-btn">
                                        Refresh Graph
                                    </b-button>
                                </div>

                                <div class="column">
                                    <b-button
                                        @click="resetFilters"
                                        type="is-danger refresh-btn">
                                        Reset Filters
                                    </b-button>
                                </div>
                            </div>
                        </div>
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
            filteredClasses: [],
            selectedClasses: [],
            graph: {
                nodes: [],
                links: []
            },
            graphOptions: {
                nodeSize: 45,
                nodeLabels: true,
                linkLabels:true,
                force: 4500
            }
        }
    },
    methods: {
        getFilteredTags (text) {
            this.filteredClasses = this.classes.filter((option) => {
                // The option must not have been chosen yet and match the partial
                // text typed in the input field
                return !this.selectedClasses.includes(option) && option.toLowerCase().indexOf(text.toLowerCase()) >= 0
            })
        },
        tagListEdited () {
            // When a tag is added/removed filter the allowable tags
            // to the ones not chosen yet
            this.filteredClasses = this.classes.filter((option) => {
                return !this.selectedClasses.includes(option)
            });
        },
        refreshGraph () {
            let filteredNodes = mockGraph.nodes.filter(node => this.selectedClasses.includes(node.class));
            let filteredNodesIDs = filteredNodes.map(node => node.id);
            let filteredEdges = mockGraph.edges.filter(edge => filteredNodesIDs.includes(edge.sid) && filteredNodesIDs.includes(edge.tid));

            this.graph.nodes = filteredNodes;
            this.graph.links = filteredEdges;
        },
        resetFilters () {
            this.graph.nodes = mockGraph.nodes;
            this.graph.links = mockGraph.edges;
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
    border-radius: 0px;
}

.app-sidebar > .panel-heading {
    border-radius: 0px;
    background-color: #7957d5;
    color: white;
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

.entities-tag-input {
    width: 100%;
}

.buttons-container {
    padding-left: 0px;
    padding-right: 0px;
}

.buttons-container > .columns > .column {
    padding-right: 0px;
}

.buttons-container > .columns {
    padding-right: 0.75rem;
}

</style>