<script>
    import Calendar from "$lib/components/Calendar.svelte";
    import {Button, Flex, TextInput} from "@svelteuidev/core";
</script>

<Flex>
    <TextInput label="From" />
    <TextInput label="To" />
    <Calendar label="Departure"/>
</Flex>
<Button>Search</Button>

