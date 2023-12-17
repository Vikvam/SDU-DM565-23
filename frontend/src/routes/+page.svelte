<script>
    import Calendar from "$lib/components/Calendar.svelte";
    import {Button, Flex, TextInput} from "@svelteuidev/core";
    import Journey from "$lib/components/Journey.svelte";

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
        if (response.status === 200) console.log(await response.json());
    }


    let journey = [
                {
                    "departure_place_name": "Campus Odense (Odense Letbane)",
                    "arrival_place_name": "Odense Banegård (Odense Letbane)",
                    "departure_datetime": "2023-12-16T18:41:00Z",
                    "arrival_datetime": "2023-12-16T18:59:00Z",
                    "transit_line": {
                        "line_name": "L",
                        "vehicle_type": "Tram",
                        "transit_agencies": [
                            {
                                "name": "Odense Letbane",
                                "uri": "https://www.odenseletbane.dk/"
                            }
                        ]
                    },
                    "price": 12
                },
                {
                    "departure_place_name": "Odense st - Gleis 3",
                    "arrival_place_name": "Kolding st",
                    "departure_datetime": "2023-12-16T19:13:00Z",
                    "arrival_datetime": "2023-12-16T19:49:00Z",
                    "transit_line": {
                        "line_name": "IC",
                        "vehicle_type": "Train",
                        "transit_agencies": [
                            {
                                "name": "DSB",
                                "uri": "http://www.dsb.dk/"
                            }
                        ]
                    },
                    "price": 5
                },
                {
                    "departure_place_name": "Kolding",
                    "arrival_place_name": "ZOB Hamburg",
                    "departure_datetime": "2023-12-16T20:50:00Z",
                    "arrival_datetime": "2023-12-17T00:40:00Z",
                    "transit_line": {
                        "line_name": "FlixBus N74",
                        "vehicle_type": "Bus",
                        "transit_agencies": [
                            {
                                "name": "FlixBus",
                                "uri": "https://global.flixbus.com/"
                            }
                        ]
                    },
                    "price": 7
                }
            ]
</script>

<div>
    <TextInput label="From" bind:value={from} />
    <TextInput label="To" bind:value={to} />
    <Calendar label="Departure" date={departure}/>
    <Button on:click={onSearch}>Search</Button>
</div>

<Journey connections={journey}/>

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

