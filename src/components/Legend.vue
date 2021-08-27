<template>
    <div class="panel-block">
        <b-field label="Legend" style="width: 100%;">
            <div>
                <div class="level legend-level">
                    <div class="level-left">
                        <div class="legend-icon level-item">
                            <svg xmlns="http://www.w3.org/2000/svg" height="32px" viewBox="0 0 24 24" width="32px" fill="#000000"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M12 7V3H2v18h20V7H12zM6 19H4v-2h2v2zm0-4H4v-2h2v2zm0-4H4V9h2v2zm0-4H4V5h2v2zm4 12H8v-2h2v2zm0-4H8v-2h2v2zm0-4H8V9h2v2zm0-4H8V5h2v2zm10 12h-8v-2h2v-2h-2v-2h2v-2h-2V9h8v10zm-2-8h-2v2h2v-2zm0 4h-2v2h2v-2z"/></svg>
                        </div>
                        <p class="level-item">Company</p>
                    </div>
                </div>

                <div class="level legend-level">
                    <div class="level-left">
                        <div class="legend-icon level-item">
                            <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="32px" viewBox="0 0 24 24" width="32px" fill="#000000"><path d="M0,0h24v24H0V0z" fill="none"/><g><path d="M19.5,3.5L18,2l-1.5,1.5L15,2l-1.5,1.5L12,2l-1.5,1.5L9,2L7.5,3.5L6,2v14H3v3c0,1.66,1.34,3,3,3h12c1.66,0,3-1.34,3-3V2 L19.5,3.5z M15,20H6c-0.55,0-1-0.45-1-1v-1h10V20z M19,19c0,0.55-0.45,1-1,1s-1-0.45-1-1v-3H8V5h11V19z"/><rect height="2" width="6" x="9" y="7"/><rect height="2" width="2" x="16" y="7"/><rect height="2" width="6" x="9" y="10"/><rect height="2" width="2" x="16" y="10"/></g></svg>
                        </div>
                        <p class="level-item">Transaction</p>
                    </div>
                </div>

                <div class="level legend-level">
                    <div class="level-left">
                        <div class="legend-icon level-item">
                            <svg xmlns="http://www.w3.org/2000/svg" height="32px" viewBox="0 0 24 24" width="32px" fill="#000000"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M12 6c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2m0 10c2.7 0 5.8 1.29 6 2H6c.23-.72 3.31-2 6-2m0-12C9.79 4 8 5.79 8 8s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm0 10c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
                        </div>
                        <p class="level-item">Person</p>
                    </div>
                </div>

                <div class="level legend-level">
                    <div class="level-left">
                        <div class="legend-icon level-item">
                            <svg xmlns="http://www.w3.org/2000/svg" height="32px" viewBox="0 0 24 24" width="32px" fill="#000000"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM4 12c0-.61.08-1.21.21-1.78L8.99 15v1c0 1.1.9 2 2 2v1.93C7.06 19.43 4 16.07 4 12zm13.89 5.4c-.26-.81-1-1.4-1.9-1.4h-1v-3c0-.55-.45-1-1-1h-6v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41C17.92 5.77 20 8.65 20 12c0 2.08-.81 3.98-2.11 5.4z"/></svg>
                        </div>
                        <p class="level-item">Country</p>
                    </div>
                </div>

                <div class="level legend-level">
                    <div class="level-left">
                        <div class="legend-color level-item" :style="`background-color: #7957D5;`"></div>
                        <p class="level-item">Original Entities</p>
                    </div>
                </div>

                <div class="level legend-level">
                    <div class="level-left">
                        <div class="legend-color level-item" :style="`background-color: #F14668;`"></div>
                        <p class="level-item">Selected Entity</p>
                    </div>
                </div>
            </div>
        </b-field>
    </div>
</template>

<script>

export default {
    name: "Legend"
}

</script>

<style scoped>

.legend-icon {
    margin-right: 16px;
}

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

.tag {
    margin-left: 4px;
    margin-right: 4px;
}

</style>