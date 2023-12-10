<script>
	import "dayjs/locale/en-gb";
	import { Month } from '@svelteuidev/dates';
    import {Container, Flex, TextInput} from "@svelteuidev/core";
    import { useFocusWithin } from '@svelteuidev/composables';

    export let label = "";
    let value = new Date();

    const [showCalendar, ref] = useFocusWithin();
</script>


<Flex use={[[ref]]} style="position: relative">
    <TextInput label={label} disabled={$showCalendar} value={value.toLocaleDateString()}/>
    <div class="popup">
        {#if $showCalendar}
            <Month month={value} date={value} onChange={(val) => value = val} locale="en-gb" />
        {/if}
    </div>
</Flex>


<style>
    .popup {
        position: absolute;
        top: calc(100% + 1rem);
    }
</style>