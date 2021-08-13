<template>
    <div class="panel-block">
        <b-field label="Legend" style="width: 100%;">
            <div v-if="graphVisible">
                <div v-for="key in Object.keys(legendDictionary)" :key="key" class="level legend-level">
                    <div class="level-left">
                        <div class="legend-color level-item" :style="`background-color: ${legendDictionary[key]};`"></div>
                        <p class="level-item">{{ key }}</p>
                    </div>
                </div>
            </div>
            <div v-if="!graphVisible">
                <p>No graph loaded</p>
            </div>
        </b-field>
    </div>
</template>

<script>

export default {
    name: "Legend",
    props: {
        graphVisible: Boolean,
        legendDictionary: Object
    }
}

</script>

<style scoped>

.legend-color {
    width: 32px;
    height: 32px;
    background-color: red;
    border-radius: 6px;
    margin-right: 16px;
}

.legend-level {
    margin-bottom: 0.5rem;
}

</style>