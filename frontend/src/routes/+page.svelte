<script>
    import Calendar from "$lib/components/Calendar.svelte";
    import {Button, Flex, TextInput} from "@svelteuidev/core";

    let from = "";
    let to = "";
    let departure = new Date();

    async function onSearch() {
        const requestBody = {from_name: from, to_name: to, departure: departure.toLocaleDateString()};
        console.log(requestBody);
        const response = await fetch("http://localhost:8000/search", {
            method: "POST",
            body: JSON.stringify(requestBody),
            mode: "cors",
            headers: {"Content-Type": "application/json"}
        })
        console.log(response);
    }
</script>

<Flex>
    <TextInput label="From" bind:value={from} />
    <TextInput label="To" bind:value={to} />
    <Calendar label="Departure" date={departure}/>
</Flex>
<Button on:click={onSearch}>Search</Button>

