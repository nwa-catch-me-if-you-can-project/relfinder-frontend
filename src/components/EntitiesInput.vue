<template>
    <div>
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
    </div>
</template>

<script>

export default {
    name: "EntitiesInput",
    data: function () {
        return {
            entities: [],
            entityTags: [],
            filteredEntityTags: [],
            selectedEntityTags: []
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
        refreshGraph () {
            this.$emit("refreshGraph", this.selectedEntityTags);
        },
        resetFilters () {
            this.$emit("resetFilters");
        },
    },
    mounted: function () {
        this.fetchEntities();
    }
}

</script>

<style scoped>

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