<script>
    import Calendar from "$lib/components/Calendar.svelte";
    import {Button, Flex, Loader, TextInput} from "@svelteuidev/core";
    import Journey from "$lib/components/Journey.svelte";
    import {onMount} from "svelte";

    let from = "Odense";
    let to = "Berlin";
    let departure = new Date("01/19/2024, 7:36:50 PM");

    async function test() {
        console.log("Requested test.")
        const response = await fetch("http://localhost:8000/search_example", {method: "GET"})
        console.log("Response:", response);
    }
    onMount(test)

    async function onSearch() {
        const requestBody = {from_name: from, to_name: to, departure: departure.toLocaleDateString()};
        isLoading = true;
        console.log("Sent request:", requestBody);
        const response = await fetch("https://localhost:8000/search", {
            method: "POST",
            body: JSON.stringify(requestBody),
            mode: "cors",
            headers: {"Content-Type": "application/json"}
        })
        isLoading = false;
        console.log("Response:", response);
        if (response.status === 200) {
            let json = await response.json();
            jouneys = json["routes"].map(i => i["legs"]);
        }
    }

    let isLoading = false;
    let jouneys = [];

    let journey = [
                {
                    "departure_place_name": "Odense St.",
                    "arrival_place_name": "Kolding st",
                    "departure_datetime": "2023-12-16T18:13:00Z",
                    "arrival_datetime": "2023-12-16T18:49:00Z",
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
                    "price": 12
                },
                {
                    "departure_place_name": "Kolding st",
                    "arrival_place_name": "Flensburg",
                    "departure_datetime": "2023-12-16T18:58:00Z",
                    "arrival_datetime": "2023-12-16T20:07:00Z",
                    "transit_line": {
                        "line_name": "IC",
                        "vehicle_type": "Train",
                        "transit_agencies": [
                            {
                                "name": "DSB",
                                "uri": "http://www.dsb.dk/"
                            },
                            {
                                "name": "Dänische Staatsbahnen",
                                "uri": "https://www.thetrainline.com/de/bahnunternehmen/dsb"
                            }
                        ]
                    },
                    "price": 16
                },
                {
                    "departure_place_name": "Flensburg",
                    "arrival_place_name": "Neumünster",
                    "departure_datetime": "2023-12-16T20:15:00Z",
                    "arrival_datetime": "2023-12-16T21:22:00Z",
                    "transit_line": {
                        "line_name": "RE7",
                        "vehicle_type": "Train",
                        "transit_agencies": [
                            {
                                "name": "DB Regio AG",
                                "uri": "http://www.bahn.de/"
                            },
                            {
                                "name": "Hamburger Verkehrsverbund (hvv)",
                                "uri": "http://www.hvv.de/"
                            }
                        ]
                    },
                    "price": 14
                },
                {
                    "departure_place_name": "Neumünster",
                    "arrival_place_name": "Hamburg Central Station",
                    "departure_datetime": "2023-12-16T21:28:00Z",
                    "arrival_datetime": "2023-12-16T22:17:00Z",
                    "transit_line": {
                        "line_name": "RE7",
                        "vehicle_type": "Train",
                        "transit_agencies": [
                            {
                                "name": "DB Regio AG",
                                "uri": "http://www.bahn.de/"
                            },
                            {
                                "name": "Hamburger Verkehrsverbund (hvv)",
                                "uri": "http://www.hvv.de/"
                            }
                        ]
                    },
                    "price": 13
                },
                {
                    "departure_place_name": "Hamburg Central Station",
                    "arrival_place_name": "München Hauptbahnhof",
                    "departure_datetime": "2023-12-16T22:28:00Z",
                    "arrival_datetime": "2023-12-17T06:04:00Z",
                    "transit_line": {
                        "line_name": "ICE1081",
                        "vehicle_type": "High-speed train",
                        "transit_agencies": [
                            {
                                "name": "DB Fernverkehr AG",
                                "uri": "https://www.bahn.de/"
                            }
                        ]
                    },
                    "price": 34
                }
            ]
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

