<script>
    import Calendar from "$lib/components/Calendar.svelte";
    import {Button, Flex, Loader, TextInput} from "@svelteuidev/core";
    import Journey from "$lib/components/Journey.svelte";
    import {onMount} from "svelte";

    let from = "Odense";
    let to = "Berlin";
    let departure = new Date("01/19/2024, 7:36:50 PM");

    // async function test() {
    //     console.log("Requested test.")
    //     const response = await fetch("http://localhost:8000/search_example", {method: "GET"})
    //     console.log("Response:", response);
    //     if (response.status === 200) {
    //         console.log(await response.json());
    //     }
    // }
    // onMount(test)

    async function onSearch() {
        const requestBody = {from_name: from, to_name: to, departure: departure.toISOString()};
        isLoading = true;
        jouneys = [];
        console.log("Sent request:", requestBody);
        const response = await fetch("http://localhost:8000/search", {
            method: "POST",
            body: JSON.stringify(requestBody),
            // mode: "cors",
            headers: {"Content-Type": "application/json"}
        })
        isLoading = false;
        console.log("Response:", response);
        if (response.status === 200) {
            let json = await response.json();
            jouneys = json["routes"].map(i => i["legs"]);
            console.log(jouneys);
        }
    }

    let isLoading = false;
    let jouneys = [];
</script>

<div>
    <TextInput label="From" bind:value={from} />
    <TextInput label="To" bind:value={to} />
    <Calendar label="Departure" date={departure}/>
    <Button on:click={onSearch}>Search</Button>
</div>

{#if jouneys.length > 0}
    {#each jouneys as journey}
        <Journey connections={journey}/>
    {/each}
{:else if isLoading}
    <Loader variant='circle' />
{/if}

<style>
    :global(body) {
        padding: 5rem 15vw;
    }
    div {
        display: flex;
        flex-direction: row;
        align-items: end;
        margin-bottom: 2rem;
    }
</style>

