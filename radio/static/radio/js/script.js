document.addEventListener("DOMContentLoaded", function () {
    console.log("TOASTS:", document.querySelectorAll(".toast").length);
    document.querySelectorAll(".toast").forEach(function (toast) {
        const toastBootstrap = new bootstrap.Toast(toast);
        toastBootstrap.show();
    });

});

// CURTIDAS

document.addEventListener("DOMContentLoaded", function () {

    const botoes = document.querySelectorAll(".btn-curtir");

    botoes.forEach(function (botao) {

        botao.addEventListener("click", function () {

            const url = botao.dataset.url;
            const idPrograma = botao.dataset.id;

            const csrfToken = botao
                .closest("form")
                .querySelector("[name=csrfmiddlewaretoken]")
                .value;

            const formData = new FormData();

            formData.append("id_programa", idPrograma);

            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": csrfToken
                }
            })
            .then(response => {

                console.log("Status:", response.status);

                return response.json();
            })
            .then(data => {

                console.log("Resposta:", data);

                const contador = botao
                    .closest("form")
                    .querySelector(".contador");

                const icone = botao.querySelector("i");

                contador.textContent = data.total_curtidas;

                if (data.curtido) {

                    icone.classList.remove(
                        "bi-heart",
                        "text-muted"
                    );

                    icone.classList.add(
                        "bi-heart-fill",
                        "text-danger"
                    );

                } else {

                    icone.classList.remove(
                        "bi-heart-fill",
                        "text-danger"
                    );

                    icone.classList.add(
                        "bi-heart",
                        "text-muted"
                    );
                }

            })
            .catch(error => {
                console.error("Erro no AJAX:", error);
            });

        });

    });

});

// PEDIDOS

const pedidoForm = document.querySelector("#pedido-form");

if (pedidoForm) {

    pedidoForm.addEventListener("submit", function (event) {

        event.preventDefault();

        const formData = new FormData(pedidoForm);

        fetch(pedidoForm.dataset.url, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": pedidoForm.querySelector(
                    "[name=csrfmiddlewaretoken]"
                ).value
            }
        })
        .then(response => response.json())
        .then(data => {

            document.querySelector("#div-mensagens").innerHTML =
                data.mensagens;

            if (data.sucesso) {
                pedidoForm.reset();
            }

            document
                .querySelectorAll("#div-mensagens .toast")
                .forEach(function (toast) {

                    const toastBootstrap =
                        new bootstrap.Toast(toast);

                    toastBootstrap.show();

                });

        })
        .catch(error => {
            console.error("Erro no AJAX:", error);
        });
    });
}

// SUGESTÃO

const sugestaoForm =
        document.querySelector("#sugestao-form");

    if (sugestaoForm) {

        sugestaoForm.addEventListener("submit", function (event) {

            event.preventDefault();

            const formData =
                new FormData(sugestaoForm);

            fetch(sugestaoForm.dataset.url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken":
                        sugestaoForm.querySelector(
                            "[name=csrfmiddlewaretoken]"
                        ).value
                }
            })
            .then(response => response.json())
            .then(data => {

                document.querySelector("#div-mensagens").innerHTML =
                    data.mensagens;

                if (data.sucesso) {
                    sugestaoForm.reset();
                }

                document
                    .querySelectorAll("#div-mensagens .toast")
                    .forEach(function (toast) {

                        const toastBootstrap =
                            new bootstrap.Toast(toast);

                        toastBootstrap.show();

                    });

            })
            .catch(error => {
                console.error(
                    "Erro no AJAX da sugestão:",
                    error
                );
            });

        });

    }

// =========================
// PROGRAMAÇÃO
// =========================

const diasSemana = document.querySelectorAll(
    ".dia-card[data-url]"
);

const programacaoConteudo = document.querySelector(
    "#programacao-conteudo"
);

if (diasSemana.length && programacaoConteudo) {

    diasSemana.forEach(function (dia) {

        dia.addEventListener("click", function (event) {

            event.preventDefault();

            fetch(dia.dataset.url)
                .then(response => response.text())
                .then(html => {

                    // Troca os cards
                    programacaoConteudo.innerHTML = html;

                    // Troca o botão ativo
                    diasSemana.forEach(function (item) {
                        item.classList.remove("ativo");
                    });

                    dia.classList.add("ativo");

                    // Atualiza a URL sem recarregar
                    history.pushState(
                        {},
                        "",
                        dia.href
                    );

                })
                .catch(error => {

                    console.error(
                        "Erro ao carregar programação:",
                        error
                    );

                });

        });

    });

}
