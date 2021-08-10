<template>
    <div class="container is-fluid app-container">
        <div class="columns">
            <div class="column is-4 is-5-tablet is-3-fullhd app-sidebar-col">
                <nav class="panel app-sidebar">
                    <p class="panel-heading">
                        UM-IDS RelFinder
                    </p>
                    <div class="panel-block">
                        <b-field label="Select Entities" class="entities-tag-input">
                            <b-taginput
                                v-model="selectedEntityTags"
                                :data="filteredEntityTags"
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
                                        @click="executeQuery"
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

                    <div class="panel-block">
                        <b-field label="Maximum Distance" class="entities-tag-input">
                            <b-slider
                                size="is-medium"
                                :min="0"
                                :max="6"
                                v-model="maxDistance">
                                <template v-for="v in [1, 2, 3, 4, 5, 6]">
                                    <b-slider-tick :value="v" :key="v">{{ v }}</b-slider-tick>
                                </template>
                            </b-slider>
                        </b-field>
                    </div>
                </nav>
            </div>
            <div class="column rel-network-col">
                <b-loading v-model="isLoading"></b-loading>

                <svg style="height: 0vh; position: absolute">
                    <defs>
                        <marker id="m-end" markerWidth="10" markerHeight="10" refX="19" refY="3" orient="auto" markerUnits="strokeWidth" >
                            <path d="M0,0 L0,6 L9,3 z"></path>
                        </marker>
                    </defs>
                </svg>

                <p v-if="!graphVisible" class="graph-info-label">Select two or more entities and press <b>Refresh Graph</b> to begin</p>

                <d3-network
                    v-if="graphVisible"
                    class="rel-network"
                    ref="relationship-network"
                    :net-nodes="this.graph.nodes"
                    :net-links="this.graph.links"
                    :options="graphOptions"
                    :link-cb="customizeLink"
                    @link-click="getLinkProperties"
                    @node-click="getEntityDataProperties" />
            </div>
        </div>
    </div>
</template>

<script>

import Values from 'values.js'
import D3Network from 'vue-d3-network'
var randomColor = require('randomcolor')

export default {
    name: "GraphBrowser",
    components: {
        D3Network
    },
    data: function () {
        return {
            entities: [],
            entityTags: [],
            filteredEntityTags: [],
            selectedEntityTags: [],
            graph: {
                nodes: [],
                links: []
            },
            graphOptions: {
                nodeSize: 50,
                nodeLabels: true,
                linkLabels: true,
                force: 25000,
                linkWidth: 2,
                strLinks: true
            },
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
            maxDistance: 2,
            isLoading: false
        }
    },
    computed: {
        graphVisible: function () {
            return this.graph.nodes.length > 0 && this.graph.links.length > 0;
        }
    },
    methods: {
        getFilteredTags (text) {
            this.filteredEntityTags = this.entityTags.filter((option) => {
                // The option must not have been chosen yet and match the partial
                // text typed in the input field
                return !this.selectedEntityTags.includes(option) && option.toLowerCase().indexOf(text.toLowerCase()) >= 0
            })
        },
        tagListEdited () {
            // When a tag is added/removed filter the allowable tags
            // to the ones not chosen yet
            this.filteredEntityTags = this.entityTags.filter((option) => {
                return !this.selectedEntityTags.includes(option)
            });
        },
        resetFilters () {
            this.selectedEntityTags = [];
            this.graph.nodes = [];
            this.graph.links = [];
        },
        refreshEntityTags (entities) {
            let entityTags = [];

            for (let i = 0; i < entities.length; i++) {
                let iri = entities[i].iri.replaceAll(
                    process.env.VUE_APP_KG_PREFIX,
                    ""
                )

                entityTags.push(`${entities[i].label} (${iri})`);
            }

            this.entityTags = entityTags;
            this.filteredEntityTags = entityTags;
        },
        fetchEntities () {
            let view = this;

            this.$store.state.api.get("entities").then(response => {
                view.entities = response.data.entities;
                view.refreshEntityTags(view.entities);
            }).catch((err) => {
                console.log(err);

                view.$buefy.toast.open({
                    message: "Could not fetch entities. Please reload the page",
                    type: "is-danger"
                })
            })
        },
        customizeLink (link) {
            link._svgAttrs = {
                "marker-end": "url(#m-end)",
            }

            return link
        },
        getEntityDataProperties (event, node) {
            let view = this;
            this.deselectNodes();

            const nodeColor = new Values(node._color);

            node._cssClass = "selected-node";
            node._svgAttrs.stroke = nodeColor.shade(12).hexString();

            this.selectedEntity = node;

            console.log(node);

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
        getLinkProperties (event, link) {
            console.log(link);
            link._svgAttrs.stroke = "#000";
        },
        deselectNodes () {
            // Removes selection markers
            this.graph.nodes.forEach(n => {
                n._svgAttrs.stroke = null;
            })
        },
        executeQuery () {
            let view = this;
            let entityIRIs = [];

            view.isLoading = true;

            for (let i = 0; i < this.selectedEntityTags.length; i++) {
                // Extract the last string between parenthesis in the tag name
                let parenthesisMatches = this.selectedEntityTags[i].match(/\(([^)]+)\)/)
                let entityId = parenthesisMatches[parenthesisMatches.length - 1];

                // Add the IRI prefix
                let iri = `${process.env.VUE_APP_KG_PREFIX}${entityId}`

                entityIRIs.push(iri);
            }

            let payload = {
                entities: entityIRIs,
                maxDistance: this.maxDistance
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
                });

                response.data.edges.forEach(e => {
                    e._color = "#000000";
                    e.name = e.label;
                });

                view.graph.nodes = response.data.nodes;
                view.graph.links = response.data.edges;

                // Assign colors to nodes
                let classColorDictionary = {};

                response.data.classes.forEach(graphClass => {
                    classColorDictionary[graphClass] = randomColor({
                        luminosity: "light"
                    });
                })

                view.graph.nodes.forEach(n => {
                    n._color = classColorDictionary[n.class]
                })

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
        updateLinkLabels () {
            // Shift back the arrow labels to avoid them
            // being covered by the nodes
            let textPaths = document.getElementsByTagName("textPath");

            for (let i = 0; i < textPaths.length; i++) {
                textPaths[i].setAttribute("startOffset", "10%");
            }
        }
    },
    created: function () {
        this.fetchEntities();
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

.graph-info-label {
    top: 40%;
    position: relative;
    text-align: center;
}

#m-end path {
  fill: #E5E5E5;
}

.property-table-container {
    margin-top: 16px;
    margin-left: 16px;
    margin-right: 16px;
}

.panel-block {
    padding: 16px;
}

</style>

<style>

.link {
    stroke: #E5E5E5 !important;
}

.node-label {
    font-weight: bold;
    font-size: 12px;
}

textPath {
    font-size: 12px;
}

.link-label {
    transform: translate(0, -16px);
    z-index: 100;
}

.selected-node {
    stroke-width: 5;
}

</style>