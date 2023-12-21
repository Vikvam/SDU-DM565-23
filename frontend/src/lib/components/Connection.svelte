<script>
    import {Text} from "@svelteuidev/core";


    export let departure;
    export let arrival;
    export let departureDatetime;
    export let arrivalDatetime;
    export let lineName;
    export let vehicleType;
    export let transitAgencies;
    export let price;

    let getImageSrc = (transitAgency) => transitAgency.toLowerCase();
</script>

<div class="connection">
    <div class="connection-meta">
        <img class="vehicle-type" src={`/vehicle-type/${vehicleType.toLowerCase()}.svg`} />
        <Text>{lineName}</Text>
    </div>
    <div class="place-box place-box-left">
        <Text weight={"bold"}>{departure.name}</Text>
        <Text>{departureDatetime.date}</Text>
        <Text>{departureDatetime.time}</Text>
    </div>
    <div class="place-box place-box-right">
        <Text weight={"bold"}>{arrival.name}</Text>
        <Text>{arrivalDatetime.date}</Text>
        <Text>{arrivalDatetime.time}</Text>
    </div>
    <div class="price">
        <Text weight={"bold"}>{price ? `${price.amount} ${price.currency}` : "?"}</Text>
    </div>
</div>

<style>
    .connection {
        height: 4rem;
        display: grid;
        grid-template-columns: .5fr repeat(2, 1fr) .5fr;
        justify-content: space-between;
        margin: var(--svelteui-space-10);
        padding: var(--svelteui-space-10);
    }
    .place-box {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .place-box-right {
        text-align: right;
    }
    .connection-meta {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        padding-right: 8%;
        margin-right: 40%;
        border-right: 2px dashed var(--svelteui-colors-gray500);
    }
    .vehicle-type {
        width: 2rem;
        height: 2rem;
    }
    .price {
        display: flex;
        align-items: center;
        justify-content: center;
        padding-left: 8%;
        margin-left: 40%;
        border-left: 2px dashed var(--svelteui-colors-gray500);
    }
</style>