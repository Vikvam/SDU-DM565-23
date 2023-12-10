<script>
    import Navigation from "$lib/components/Navigation.svelte";
    import {SvelteUIProvider} from "@svelteuidev/core";
    // import {fns, AppShell, Navbar, Header, Title, Divider, ShellSection} from '@svelteuidev/core';
    //
    // let isDark = false;
	// let opened = false;
    //
	// function toggleTheme() {
	// 	isDark = !isDark;
	// }
	// function toggleOpened() {
	// 	opened = !opened;
	// }
</script>

<SvelteUIProvider>
<!--    <Navigation />-->
    <slot />
<!--    <AppShell>-->
<!--    &lt;!&ndash;    <Navigation />&ndash;&gt;-->
<!--        <Navbar slot="navbar" hidden={!opened}>-->
<!--            <ShellSection>First section</ShellSection>-->
<!--            <ShellSection grow>Grow section</ShellSection>-->
<!--            <ShellSection>Last section</ShellSection>-->
<!--        </Navbar>-->
<!--        <Header slot="header">-->
<!--            Header-->
<!--        </Header>-->
<!--        <slot />-->
<!--    </AppShell>-->
</SvelteUIProvider>