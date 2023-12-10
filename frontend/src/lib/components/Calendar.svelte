<script>
	import "dayjs/locale/en-gb";
	import { Month } from '@svelteuidev/dates';
    import {Container, Flex, TextInput} from "@svelteuidev/core";
    import { useFocusWithin } from '@svelteuidev/composables';

    export let label = "";
    export let date = new Date();

    const [showCalendar, ref] = useFocusWithin();
</script>


<Flex use={[[ref]]} style="position: relative">
    <TextInput label={label} disabled={$showCalendar} value={date.toLocaleDateString()}/>
    <div class="popup">
        {#if $showCalendar}
            <Month month={date} date={date} onChange={(val) => date = val} locale="en-gb" />
        {/if}
    </div>
</Flex>


<style>
    .popup {
        position: absolute;
        top: calc(100% + 1rem);
    }
</style>