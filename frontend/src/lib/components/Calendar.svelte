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
    {#if $showCalendar}
    <div class="popup">
        <Month month={date} date={date} onChange={(val) => date = val} locale="en-gb" />
    </div>
    {/if}
</Flex>


<style>
    .popup {
        position: absolute;
        top: calc(100%);
        padding-top: 1rem;
        border-radius: var(--svelteui-radii-sm);
        background-color: var(--svelteui-colors-white);
        border: 1px solid var(--svelteui-colors-gray200);
    }
</style>