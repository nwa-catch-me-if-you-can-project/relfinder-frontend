<!-- Copyright (C) <2021>  <Kody Moodley and Walter Simoncini> -->
<!-- License: https://www.gnu.org/licenses/agpl-3.0.txt -->

<template>
    <div class="container is-fluid app-container">
        <div class="columns">
            <div class="column is-4 is-5-tablet is-3-fullhd app-sidebar-col">
                <nav class="panel app-sidebar">
                    <p class="panel-heading">
                        RelFinder
                    </p>

                    <EntitiesInput
                        @refreshGraph="executeQuery"
                        @resetFilters="resetFilters" />

                    <OptionsPanel
                        @toggleLinkLabels="toggleEdgeLabels" />

                    <Legend />

                    <div
                        v-if="selectedEntity"
                        class="property-table-container">
                        <h3 class="subtitle">Entity properties</h3>
                        <p>
                            Data properties of entity
                            <b>{{ selectedEntity.label }}</b>
                            of class
                            <b>{{ selectedEntity.class }}</b>
                            with IRI
                            <b>{{ selectedEntity.iri }}</b>
                        </p>

                        <br/>

                        <b-table
                            :data="entityTableData"
                            :columns="entityTableColumns">
                        </b-table>
                    </div>
                </nav>
            </div>

            <div class="column rel-network-col">
                <b-loading v-model="isLoading"></b-loading>

                <svg style="height: 0vh; position: absolute">
                    <defs>
                        <marker
                            id="m-end"
                            markerWidth="10"
                            markerHeight="10"
                            refX="19"
                            refY="3"
                            orient="auto"
                            markerUnits="strokeWidth">
                            <path d="M0,0 L0,6 L9,3 z"></path>
                        </marker>

                        <marker
                            id="m-end-endpoint"
                            markerWidth="10"
                            markerHeight="10"
                            refX="22"
                            refY="3"
                            orient="auto"
                            markerUnits="strokeWidth">
                            <path d="M0,0 L0,6 L9,3 z"></path>
                        </marker>
                    </defs>
                </svg>

                <p v-if="!graphVisible" class="graph-info-label">Select two or more entities and press <b>Refresh Graph</b> to begin</p>

                <d3-network
                    v-if="graphVisible"
                    class="rel-network"
                    ref="relationshipNetwork"
                    :net-nodes="this.graph.nodes"
                    :net-links="this.graph.displayedLinks"
                    :options="graphOptions"
                    :link-cb="customizeLink"
                    @node-click="getEntityDataProperties" />
            </div>

            <b-button
                type="is-primary"
                id="screenshot-button"
                @click="takeScreenshot">
                Screenshot
            </b-button>
        </div>
    </div>
</template>

<script>

import D3Network from 'vue-d3-network'
import iconsMapping from '@/assets/icons.js';

import Legend from '@/components/Legend.vue';
import OptionsPanel from '@/components/OptionsPanel.vue';
import EntitiesInput from '@/components/EntitiesInput.vue';

export default {
    name: "GraphBrowser",
    components: {
        Legend,
        D3Network,
        OptionsPanel,
        EntitiesInput
    },
    data: function () {
        return {
            graph: {
                nodes: [],
                links: [],
                // Links which are presented to the user. This property is used
                // to handle showing/hiding edge labels dynamically
                displayedLinks: []
            },
            graphOptions: {
                nodeSize: 50,
                nodeLabels: true,
                linkLabels: true,
                force: 50000,
                linkWidth: 2,
                strLinks: true
            },
            showLinkLabels: true,
            selectedEntity: null,
            entityTableData: [],
            entityTableColumns: [
                {
                    field: "property",
                    label: "Property"
                },
                {
                    field: "value",
                    label: "Value",
                    // Needed to align the cell to the right
                    numeric: true
                }
            ],
            isLoading: false,
            legendColors: {
                selected: "#F14668",
                endpoint: "#7957D5",
                default: "#000000"
            }
        }
    },
    computed: {
        graphVisible: function () {
            return this.graph.nodes.length > 0 && this.graph.links.length > 0;
        }
    },
    methods: {
        takeScreenshot () {
            let timestamp = Math.floor(Date.now() / 1000);

            this.$refs.relationshipNetwork.screenShot(
                `relfinder-${timestamp}.png`,
                "#FFFFFF",
                false,
                true
            );
        },
        resetFilters () {
            this.selectedEntityTags = [];
            this.graph.nodes = [];
            this.graph.links = [];
        },
        customizeLink (link) {
            if (link.tid == 0 || link.tid == 1) {
                // Special customizations for source and destination nodes
                link._svgAttrs = {
                    "marker-end": "url(#m-end-endpoint)"
                }
            } else {
                link._svgAttrs = {
                    "marker-end": "url(#m-end)",
                }
            }

            return link
        },
        getEntityDataProperties (event, node) {
            let view = this;
            this.deselectNodes();

            node._color = this.legendColors.selected;

            this.selectedEntity = node;

            this.$store.state.api.post("entities/properties", {iri: node.iri}).then(response => {
                console.log(response.data);

                let propertyData = [];

                response.data.properties.forEach(prop => {
                    propertyData.push({
                        property: prop.label,
                        value: prop.value
                    });
                });

                view.entityTableData = propertyData;
            }).catch((err) => {
                console.log(err);

                view.$buefy.toast.open({
                    message: "Could not fetch the entity properties. Please reload the page",
                    type: "is-danger"
                })
            })
        },
        deselectNodes () {
            let view = this;

            // Removes selection markers
            this.graph.nodes.forEach(n => {
                if (!n.isEndpoint) {
                    n._color = view.legendColors.default;
                } else {
                    n._color = view.legendColors.endpoint;
                }
            })
        },
        executeQuery (selectedEntityTags) {
            let view = this;
            let entityIRIs = [];

            view.isLoading = true;

            for (let i = 0; i < selectedEntityTags.length; i++) {
                // Extract the last string between parenthesis in the tag name
                const parenthesisMatches = [...selectedEntityTags[i].matchAll(/\(([^)]+)\)/g)];
                const matchesArray = parenthesisMatches[parenthesisMatches.length - 1];

                let entityId = matchesArray[matchesArray.length - 1];

                // Add the IRI prefix if not present yet
                let iri = `${process.env.VUE_APP_KG_PREFIX}${entityId}`

                if (entityId.includes("http")) {
                    iri = entityId;
                }

                entityIRIs.push(iri);
            }

            if (entityIRIs.length != 2) {
                view.$buefy.toast.open({
                    message: "Queries can only be performed between two objects",
                    type: "is-danger",
                    duration: 5000
                })

                view.isLoading = false;

                return;
            }

            let payload = {
                entities: entityIRIs,
                maxDistance: this.$store.state.maxDistance
            }

            this.$store.state.api.post("query", payload).then(response => {
                if (response.data.edges.length == 0) {
                    view.$buefy.toast.open({
                        message: `There are no connections between the selected entities (max distance ${payload.maxDistance})`,
                        type: "is-danger",
                        duration: 5000
                    })

                    view.isLoading = false;
                    
                    return
                }

                response.data.nodes.forEach(n => {
                    n.name = n.label;
                    n._svgAttrs = {};

                    if (n.class in iconsMapping) {
                        n.svgSym = iconsMapping[n.class];
                    }

                    if (n.isEndpoint) {
                        n._size = 75;
                        n._color = view.legendColors.endpoint;
                    }
                });

                response.data.edges.forEach(e => {
                    e._color = "#000000";
                    e.name = e.label;
                });

                view.graph.nodes = response.data.nodes;
                view.graph.links = response.data.edges;

                view.refreshDisplayedLinks(response.data.edges);

                // Dirty trick to make link labels visible.
                // No method is exposed by the component to
                // monitor graph updates
                setTimeout(view.updateLinkLabels, 500);
                
                view.isLoading = false;
            }).catch((err) => {
                console.log(err);

                view.isLoading = false;

                view.$buefy.toast.open({
                    message: "Could not execute the query. Please retry later",
                    type: "is-danger"
                })
            })
        },
        refreshDisplayedLinks (links) {
            let tempLinks = JSON.parse(JSON.stringify(links));

            if (this.showLinkLabels) {
                this.graph.displayedLinks = tempLinks;
            } else {
                tempLinks.forEach(link => {
                    link.name = null;
                })

                this.graph.displayedLinks = tempLinks;
            }
        },
        updateLinkLabels () {
            // Shift back the arrow labels to avoid them
            // being covered by the nodes
            let textPaths = document.getElementsByTagName("textPath");

            for (let i = 0; i < textPaths.length; i++) {
                textPaths[i].setAttribute("startOffset", "10%");
            }
        },
        toggleEdgeLabels (value) {
            this.showLinkLabels = value;
            this.refreshDisplayedLinks(this.graph.links);
        }
    }
};

</script>

<style scoped>

.app-container {
    padding-left: 0px;
    padding-right: 0px;
}

.app-sidebar {
    height: 100%;
    min-height: 100vh;
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

.graph-info-label {
    top: 40%;
    position: relative;
    text-align: center;
}

.property-table-container {
    margin-top: 16px;
    margin-left: 16px;
    margin-right: 16px;
}

.panel-block {
    padding: 16px;
}

#screenshot-button {
    position: absolute;
    bottom: 24px;
    right: 24px;
    font-size: 20px;
}

</style>