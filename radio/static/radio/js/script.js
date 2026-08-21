document.addEventListener("DOMContentLoaded", function () {
    console.log("TOASTS:", document.querySelectorAll(".toast").length);
    document.querySelectorAll(".toast").forEach(function (toast) {
        const toastBootstrap = new bootstrap.Toast(toast);
        toastBootstrap.show();
    });

});

// =========================
// CURTIDAS
// =========================

document.addEventListener("click", function (event) {

    const botao = event.target.closest(".btn-curtir");

    if (!botao) {
        return;
    }

    event.preventDefault();

    const url = botao.dataset.url;
    const idPrograma = botao.dataset.id;

    const form = botao.closest("form");

    const csrfToken = form.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;

    const formData = new FormData();

    formData.append("id_programa", idPrograma);

    fetch(url, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {

        const contador = form.querySelector(".contador");
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
        console.error("Erro no AJAX da curtida:", error);
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

// =========================
// PESQUISA DE PROGRAMAS
// =========================

const pesquisaProgramas = document.querySelector("#pesquisa-programas");
const programasConteudo = document.querySelector("#programas-conteudo");

if (pesquisaProgramas && programasConteudo) {

    pesquisaProgramas.addEventListener("submit", function (event) {

        event.preventDefault();

        const input = pesquisaProgramas.querySelector(
            "input[name='f']"
        );

        const filtro = input.value;

        const url = pesquisaProgramas.dataset.url;

        fetch(`${url}?f=${encodeURIComponent(filtro)}`)
            .then(response => response.text())
            .then(html => {

                programasConteudo.innerHTML = html;

                // Atualiza a URL sem recarregar a página
                history.pushState(
                    {},
                    "",
                    `${url}?f=${encodeURIComponent(filtro)}`
                );

            })
            .catch(error => {
                console.error(
                    "Erro no AJAX da pesquisa:",
                    error
                );
            });

    });

}
