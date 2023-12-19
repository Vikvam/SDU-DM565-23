<script>
    import Connection from "$lib/components/Connection.svelte";
    import {Button, Collapse, Text} from '@svelteuidev/core';

    export let connections;
    connections = connections.map(i => snakeToCamel(editConnection(i)))

    let priceSum = connections.reduce((accumulator, currentJourney) => {
        if (typeof currentJourney.price === 'number' && !isNaN(currentJourney.price)) accumulator += currentJourney.price;
        return accumulator;
    }, 0);
    let isOpen = true;

    function editConnection(obj) {
        return Object.keys(obj).reduce((acc, key) => {
            if (key === "arrival_datetime" || key === "departure_datetime") {
                let date = new Date(obj[key]);
                acc[key] = {"date": date.toLocaleDateString(), "time": date.toLocaleTimeString()}
            }
            else if (key === "transit_line") for (const innerKey in obj[key]) acc[innerKey] = obj[key][innerKey];
            else acc[key] = obj[key];
            return acc;
        }, {});
    }

    function snakeToCamel(obj) {
        if (typeof obj !== 'object' || obj === null) {
            return obj;
        }

        if (Array.isArray(obj)) {
            return obj.map(snakeToCamel);
        }

        return Object.keys(obj).reduce((acc, key) => {
            const camelKey = key.replace(/_([a-z])/g, (_, match) => match.toUpperCase());
            acc[camelKey] = snakeToCamel(obj[key]);
            return acc;
        }, {});
    }
</script>

<div class="journey">
    <Button on:click={() => isOpen = !isOpen} color={isOpen ? "red" : "green"}>{isOpen ? "Collapse" : "Open"}</Button>
    <Collapse open={isOpen} transitionDuration={500}>
        {#each connections as connection}
            <Connection {...connection}/>
        {/each}
    </Collapse>
    <div class="journey-summary">
        <div class="price-sum"><Text weight={"bold"}>{priceSum}</Text></div>
    </div>
</div>

<style>
    .journey {
        box-shadow: var(--svelteui-shadows-xs);
        border: 1px solid var(--svelteui-colors-gray200);
        margin: var(--svelteui-space-10) 0;
    }
    .journey-summary {
        display: grid;
        grid-template-columns: .5fr repeat(2, 1fr) .5fr;
    }
    .price-sum {
        grid-column: 4;
        padding-left: 8%;
        margin-left: 40%;
    }
</style>