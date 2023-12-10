<script>
    import { onMount } from "svelte";
    import { Anchor } from '@svelteuidev/core';

    const navItems = [
        { label: "Item 1", href: "item_1" },
        { label: "Item 2", href: "item_2" },
        { label: "Item 3", href: "item_3" },
        { label: "Item 4", href: "item_4" },
        { label: "Item 5", href: "item_5" },
        { label: "Item 6", href: "item_6" },
        { label: "Item 7", href: "item_7" }
    ];

    let burgerNav = false;
    let burgerOpen = false;

    onMount(() => {
        const mediaListener = window.matchMedia("(max-width: 700px)");
        mediaListener.addEventListener("change", (e) => {
            burgerNav = e.matches;
            burgerOpen = !e.matches;
        });
    })
</script>

<nav>
    <ul>
    {#each navItems as item}
        <li>
            <Anchor href={item.href}>{item.label}</Anchor>
        </li>
    {/each}
    </ul>
</nav>

