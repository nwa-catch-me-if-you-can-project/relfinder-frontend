<template>
    <div class="panel-block">
        <div class="columns options-column">
            <div class="column is-8">
                <b-field label="Maximum Distance" class="entities-tag-input">
                    <b-slider
                        size="is-medium"
                        :min="1"
                        :max="6"
                        v-model="maxDistance">
                        <template v-for="v in [1, 2, 3, 4, 5, 6]">
                            <b-slider-tick :value="v" :key="v">{{ v }}</b-slider-tick>
                        </template>
                    </b-slider>
                </b-field>
            </div>

            <div class="column">
                <b-field label="Edge labels" class="entities-tag-input">
                    <b-switch
                        @input="toggleEdgeLabels"
                        v-model="showLinkLabels"
                        :true-value="true"
                        :false-value="false">
                    </b-switch>
                </b-field>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: "OptionsPanel",
    props: {
        maxDistance: Number
    },
    data: function () {
        return {
            showLinkLabels: true
        }
    },
    methods: {
        toggleEdgeLabels () {
            this.$emit("toggleLinkLabels", this.showLinkLabels);
        }
    }
}

</script>

<style scoped>

.options-column {
    width: 100%;
}

</style>