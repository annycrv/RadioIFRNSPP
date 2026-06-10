console.log("JS carregou");
const modalElemento = document.querySelector("#modal");

const meuModal = new bootstrap.Modal(modalElemento);

function buscarMensagens() {
    console.log("Buscando mensagens...");

    const divMensagens =
        document.querySelector("#div-mensagens");

    fetch(divMensagens.dataset.url)
        .then(response => response.text())
        .then(resposta => {

            divMensagens.innerHTML = resposta;

            document
                .querySelectorAll("#div-mensagens .toast")
                .forEach(function (toastEl) {

                    const toast =
                        new bootstrap.Toast(toastEl);

                    toast.show();

                });

        });
}

function atualizarLista(seletor) {

const divLista = document.querySelector(seletor);

console.log(divLista);

console.log(divLista.dataset.url);

fetch(divLista.dataset.url)

    .then(response => response.text())

    .then(html => {

        console.log(html);

        divLista.innerHTML = html;

    });

}

document.addEventListener("click", function (evento) {

const botao = evento.target.closest(".btn-novo");

if (botao) {

    evento.preventDefault();

    console.log("clicou");

    fetch(botao.href)

        .then(response => response.text())

        .then(conteudo => {

            document.querySelector(
                ".modal-title"
            ).innerHTML = botao.dataset.titulo;

            document.querySelector(
                ".modal-body"
            ).innerHTML = conteudo;

            const form =
                document.querySelector(".form-modal");

            form.action = botao.href;

            meuModal.show();

        });

}

});
document.addEventListener("click", function (evento) {

    if (evento.target.classList.contains("btn-salvar")) {
        console.log("salvando");


        const form = document.querySelector(".form-modal");

        fetch(form.action, {
            method: "POST",
            body: new FormData(form)
        })

        .then(response => response.text())

        .then(conteudo => {
            console.log(conteudo);

            if (conteudo === "ok") {

                document.activeElement.blur();

                meuModal.hide();

                atualizarLista("#container-lista");
                buscarMensagens();

            } else {

                document.querySelector(".modal-body").innerHTML =
                    conteudo;

            }

        });

    }

});

document.addEventListener("click", function (evento) {

const botao = evento.target.closest(".btn-editar");

if (botao) {

    evento.preventDefault();

    fetch(botao.href)

        .then(response => response.text())

        .then(html => {

            document.querySelector(
                "#modal .modal-body"
            ).innerHTML = html;

            const form =
                document.querySelector(".form-modal");

            form.action = botao.href;

            meuModal.show();

        });

}

});

document.addEventListener("click", function (evento) {

const botao = evento.target.closest(".detalhar");

if (botao) {

    evento.preventDefault();

    fetch(botao.href)

        .then(response => response.text())

        .then(html => {

            document.querySelector(
                "#modal .modal-body"
            ).innerHTML = html;

            meuModal.show();

        });

}

});

document.addEventListener("click", function (evento) {

const botao = evento.target.closest(".remover");

if (botao) {

    evento.preventDefault();

    fetch(botao.href)

        .then(response => response.text())

        .then(html => {

            document.querySelector(
                "#modal .modal-body"
            ).innerHTML = html;

            meuModal.show();

        });

}

});

document.addEventListener("click", function (evento) {

if (evento.target.classList.contains("confirmar")) {

    evento.preventDefault();

    const formRemover =
        document.querySelector(".form-remover");

    fetch(formRemover.action, {
        method: "POST",
        body: new FormData(formRemover)
    })

    .then(response => response.text())

    .then(conteudo => {

        if (conteudo === "ok") {

            document.activeElement.blur();

            meuModal.hide();

            atualizarLista("#container-lista");
            buscarMensagens();

        } else {

            document.querySelector(
                ".modal-body"
            ).innerHTML = conteudo;

        }

    });

}

});

