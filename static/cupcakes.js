const BASE_URL = "http://localhost:5000/api";

$('.delete-cupcake').click(deleteCupcake)

async function deleteCupcake() {
    const id = $(this).data('id');
    await axios.delete(`/api/cupcakes/${id}`);
    $(this).parent().remove();
}

function generateCupcakeHTML(cupcake) {
    return `
    <li>
    ${cupcake.flavor}
    <button class="delete-cupcake" data-id="${cupcake.id}">X</button>
    </li>
    `
}

$('#new-cupcake-form').on("submit", async function(evt) {
    evt.preventDefault();

    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });

    let newCupcake = generateCupcakeHTML(newCupcakeResponse.data.cupcake);
    $('#cupcake-list').append(newCupcake);
    $("#new-cupcake-form").trigger("reset");

})
