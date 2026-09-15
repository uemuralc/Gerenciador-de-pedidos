let todosOsPedidos = [];
let pedidoEditandoId = null;
let materialEditandoId = null;

function escaparHTML(texto) {
    if (texto === null || texto === undefined) return '';
    const mapa = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
    return String(texto).replace(/[&<>"']/g, function(m) { return mapa[m]; });
}

function mostrarToast(mensagem, tipo = 'sucesso') {
    const toast = document.getElementById("toast");
    toast.innerText = mensagem;
    toast.className = tipo === 'sucesso' ? "toast-sucesso mostrar" : "toast-erro mostrar";
    setTimeout(() => { toast.className = toast.className.replace("mostrar", ""); }, 3000);
}

function filtrarTabela(inputId, tabelaId) {
    const termo = document.getElementById(inputId).value.toLowerCase();
    const linhas = document.getElementById(tabelaId).getElementsByTagName('tr');
    for (let i = 0; i < linhas.length; i++) {
        const textoLinha = linhas[i].innerText.toLowerCase();
        linhas[i].style.display = textoLinha.includes(termo) ? '' : 'none';
    }
}

function abrirModalAdmin() {
    document.getElementById('modalSenha').style.display = 'flex';
    document.getElementById('inputSenha').value = '';
    document.getElementById('msgErro').style.display = 'none';
    setTimeout(() => document.getElementById('inputSenha').focus(), 100);
}

async function verificarSenha() {
    const senhaDigitada = document.getElementById('inputSenha').value;
    try {
        const resposta = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ senha: senhaDigitada })
        });
        const resultado = await resposta.json();
        if (resultado.sucesso) {
            fecharModalSenha();
            mostrarToast('Modo Admin ativado!', 'sucesso');
            document.getElementById('btnFilaPedidos').style.display = 'block';
            document.getElementById('btnEstoque').style.display = 'block';
            document.getElementById('btnLoginAdmin').style.display = 'none';
            document.getElementById('btnSairAdmin').style.display = 'block';
            carregarPedidos();
            carregarEstoque();
        } else {
            document.getElementById('msgErro').style.display = 'block';
        }
    } catch (e) {
        mostrarToast('Erro ao conectar com o servidor', 'erro');
    }
}

async function sairAdmin() {
    try {
        await fetch('/api/logout', { method: 'POST' });
        mudarAba('novoPedido');
        document.getElementById('btnFilaPedidos').style.display = 'none';
        document.getElementById('btnEstoque').style.display = 'none';
        document.getElementById('btnLoginAdmin').style.display = 'block';
        document.getElementById('btnSairAdmin').style.display = 'none';
        mostrarToast('Modo Admin desativado', 'sucesso');
    } catch (e) {
        mostrarToast('Erro ao sair', 'erro');
    }
}

function fecharModalSenha() { document.getElementById('modalSenha').style.display = 'none'; }

function mudarAba(abaDestino) {
    ['secaoNovoPedido', 'secaoFilaPedidos', 'secaoEstoque'].forEach(id => document.getElementById(id).style.display = 'none');
    ['btnNovoPedido', 'btnFilaPedidos', 'btnEstoque'].forEach(id => document.getElementById(id).classList.remove('ativo'));

    if (abaDestino === 'novoPedido') {
        document.getElementById('secaoNovoPedido').style.display = 'block';
        document.getElementById('btnNovoPedido').classList.add('ativo');
        setTimeout(() => document.getElementById('clienteNome').focus(), 100);
    } else if (abaDestino === 'filaPedidos') {
        document.getElementById('secaoFilaPedidos').style.display = 'block';
        document.getElementById('conteudoFila').style.display = 'block';
        document.getElementById('secaoPerfil').style.display = 'none';
        document.getElementById('btnFilaPedidos').classList.add('ativo');
    } else if (abaDestino === 'estoque') {
        document.getElementById('secaoEstoque').style.display = 'block';
        document.getElementById('btnEstoque').classList.add('ativo');
        setTimeout(() => document.getElementById('materialNome').focus(), 100);
    }
}

async function carregarPedidos() {
    try {
        const resposta = await fetch('/api/pedidos');
        todosOsPedidos = await resposta.json();
    } catch (e) {
        mostrarToast('Erro ao carregar pedidos', 'erro');
        return;
    }

    const tbody = document.getElementById('tabelaPedidos');
    tbody.innerHTML = '';

    todosOsPedidos.forEach(p => {
        let corStatus = p.status === 'Em andamento' ? '#17a2b8' : (p.status === 'Finalizado' ? 'green' : 'orange');
        let btnAcaoStatus = p.status === 'Pendente'
            ? `<button class="btn-acao bg-andamento" data-acao="iniciar" data-id="${p.id}">Iniciar</button>`
            : (p.status === 'Em andamento' ? `<button class="btn-acao bg-finalizar" data-acao="finalizar" data-id="${p.id}">Finalizar</button>` : `<span>✅</span>`);

        let anexoHtml = p.documento_url ? `<a href="${p.documento_url}" target="_blank" title="Ver Documento" style="margin-left: 10px; text-decoration: none; font-size: 18px;">📎</a>` : '';

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${p.id}</td>
            <td class="link-cliente" data-acao="perfil">${escaparHTML(p.cliente)}</td>
            <td>${escaparHTML(p.contato) || 'N/A'}</td>
            <td>${escaparHTML(p.item) || 'N/A'} ${anexoHtml}</td>
            <td>${escaparHTML(p.material_origem) || 'N/A'}</td>
            <td style="color: ${corStatus}; font-weight: bold;">${p.status}</td>
            <td>
                ${btnAcaoStatus}
                <button class="btn-acao bg-editar" data-acao="editar" data-id="${p.id}" title="Editar">✏️</button>
                <button class="btn-acao bg-deletar" data-acao="deletar" data-id="${p.id}" title="Excluir">🗑️</button>
            </td>
        `;

        tr.querySelector('.link-cliente').addEventListener('click', () => abrirPerfil(p.cliente));
        const btnStatus = tr.querySelector('[data-acao="iniciar"], [data-acao="finalizar"]');
        if (btnStatus) {
            const novoStatus = btnStatus.dataset.acao === 'iniciar' ? 'Em andamento' : 'Finalizado';
            btnStatus.addEventListener('click', () => alterarStatus(p.id, novoStatus));
        }
        tr.querySelector('[data-acao="editar"]').addEventListener('click', () => abrirModalEditar(p.id, p.cliente, p.contato, p.item, p.material_origem));
        tr.querySelector('[data-acao="deletar"]').addEventListener('click', () => deletarPedido(p.id));

        tbody.appendChild(tr);
    });
    filtrarTabela('buscaPedidos', 'tabelaPedidos');
}

async function adicionarPedido() {
    const cliente = document.getElementById('clienteNome').value;
    const contato = document.getElementById('clienteContato').value;
    const item = document.getElementById('itemPedido').value;
    const materialOrigem = document.getElementById('materialOrigem').value;
    const arquivoInput = document.getElementById('arquivoPedido');
    const arquivo = arquivoInput.files[0];

    if (!cliente || !contato || !item) return mostrarToast('Preencha os campos obrigatórios!', 'erro');

    const formData = new FormData();
    formData.append('cliente', cliente);
    formData.append('contato', contato);
    formData.append('item', item);
    formData.append('material_origem', materialOrigem);
    if (arquivo) {
        formData.append('documento', arquivo);
    }

    const btn = document.getElementById('btnCadastrarPedido');
    btn.innerText = "Enviando... Aguarde";
    btn.disabled = true;

    try {
        const resposta = await fetch('/api/pedidos', { 
            method: 'POST', 
            body: formData 
        });
        
        if (!resposta.ok) {
            const erro = await resposta.json();
            mostrarToast(erro.erro || 'Erro ao cadastrar pedido', 'erro');
        } else {
            document.getElementById('clienteNome').value = '';
            document.getElementById('clienteContato').value = '';
            document.getElementById('itemPedido').value = '';
            document.getElementById('materialOrigem').value = 'Cliente vai levar';
            arquivoInput.value = '';
            mostrarToast('Pedido cadastrado!');
            carregarPedidos();
            document.getElementById('clienteNome').focus();
        }
    } catch (e) {
        mostrarToast('Erro ao conectar com o servidor', 'erro');
    } finally {
        btn.innerText = "Cadastrar Pedido";
        btn.disabled = false;
    }
}

async function alterarStatus(id_pedido, status) {
    try {
        await fetch(`/api/pedidos/${id_pedido}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ status }) });
        mostrarToast('Status atualizado!');
        carregarPedidos();
    } catch (e) {
        mostrarToast('Erro ao atualizar status', 'erro');
    }
}

function abrirModalEditar(id, clienteAtual, contatoAtual, itemAtual, materialAtual) {
    pedidoEditandoId = id;
    document.getElementById('editCliente').value = clienteAtual;
    document.getElementById('editContato').value = contatoAtual || '';
    document.getElementById('editItem').value = itemAtual;
    document.getElementById('editMaterial').value = materialAtual || 'Cliente vai levar';
    document.getElementById('modalEditar').style.display = 'flex';
    setTimeout(() => document.getElementById('editCliente').focus(), 100);
}

function fecharModalEditar() { document.getElementById('modalEditar').style.display = 'none'; pedidoEditandoId = null; }

async function salvarEdicaoPedido() {
    const novoCliente = document.getElementById('editCliente').value;
    const novoContato = document.getElementById('editContato').value;
    const novoItem = document.getElementById('editItem').value;
    const novoMaterial = document.getElementById('editMaterial').value;

    if (!novoCliente || !novoContato || !novoItem) return mostrarToast('Preencha os campos de texto!', 'erro');

    try {
        const resposta = await fetch(`/api/pedidos/${pedidoEditandoId}`, { 
            method: 'PUT', 
            headers: { 'Content-Type': 'application/json' }, 
            body: JSON.stringify({ cliente: novoCliente, contato: novoContato, item: novoItem, material_origem: novoMaterial }) 
        });
        if (!resposta.ok) {
            const erro = await resposta.json();
            return mostrarToast(erro.erro || 'Erro ao atualizar pedido', 'erro');
        }
    } catch (e) {
        return mostrarToast('Erro ao conectar com o servidor', 'erro');
    }

    fecharModalEditar();
    mostrarToast('Pedido atualizado!');
    carregarPedidos();
}

async function deletarPedido(id) {
    if (confirm("Tem certeza que deseja excluir este pedido?")) {
        try {
            await fetch(`/api/pedidos/${id}`, { method: 'DELETE' });
            mostrarToast('Pedido excluído!', 'erro');
            carregarPedidos();
        } catch (e) {
            mostrarToast('Erro ao excluir pedido', 'erro');
        }
    }
}

function abrirPerfil(nomeCliente) {
    document.getElementById('conteudoFila').style.display = 'none';
    document.getElementById('secaoPerfil').style.display = 'block';
    document.getElementById('tituloPerfil').innerText = `Histórico de: ${nomeCliente}`;
    const pedidosDesteCliente = todosOsPedidos.filter(p => p.cliente === nomeCliente);
    const tbodyPerfil = document.getElementById('tabelaPerfil');
    tbodyPerfil.innerHTML = '';

    pedidosDesteCliente.forEach(p => {
        let corStatus = p.status === 'Em andamento' ? '#17a2b8' : (p.status === 'Finalizado' ? 'green' : 'orange');
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${p.id}</td><td>${escaparHTML(p.contato) || 'N/A'}</td><td>${escaparHTML(p.item) || 'N/A'}</td><td>${escaparHTML(p.material_origem) || 'N/A'}</td><td style="color: ${corStatus}; font-weight: bold;">${p.status}</td>`;
        tbodyPerfil.appendChild(tr);
    });
}

function fecharPerfil() { document.getElementById('conteudoFila').style.display = 'block'; document.getElementById('secaoPerfil').style.display = 'none'; }

// Funções de estoque mantidas
async function carregarEstoque() {
    let estoque;
    try {
        const resposta = await fetch('/api/estoque');
        estoque = await resposta.json();
    } catch (e) { return mostrarToast('Erro ao carregar estoque', 'erro'); }
    const tbody = document.getElementById('tabelaEstoque');
    tbody.innerHTML = '';
    estoque.forEach(mat => {
        const corQtd = mat.quantidade <= 5 ? 'red' : 'black';
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${mat.id}</td><td>${escaparHTML(mat.nome)}</td>
            <td style="color: ${corQtd}; font-weight: bold;"><button class="btn-qtd" data-acao="menos">-</button> ${mat.quantidade} <button class="btn-qtd" data-acao="mais">+</button></td>
            <td>${escaparHTML(mat.unidade)}</td>
            <td><button class="btn-acao bg-editar" data-acao="editar" title="Editar">✏️</button> <button class="btn-acao bg-deletar" data-acao="deletar" title="Excluir Material">🗑️</button></td>`;
        tr.querySelector('[data-acao="menos"]').addEventListener('click', () => atualizarQuantidade(mat.id, mat.quantidade - 1));
        tr.querySelector('[data-acao="mais"]').addEventListener('click', () => atualizarQuantidade(mat.id, mat.quantidade + 1));
        tr.querySelector('[data-acao="editar"]').addEventListener('click', () => abrirModalEditarEstoque(mat.id, mat.nome, mat.quantidade, mat.unidade));
        tr.querySelector('[data-acao="deletar"]').addEventListener('click', () => deletarEstoque(mat.id));
        tbody.appendChild(tr);
    });
    filtrarTabela('buscaEstoque', 'tabelaEstoque');
}

async function adicionarEstoque() {
    const nome = document.getElementById('materialNome').value;
    const qtd = document.getElementById('materialQtd').value;
    const unidade = document.getElementById('materialUnidade').value;
    if (!nome || !qtd) return mostrarToast('Preencha os dados!', 'erro');
    try {
        const resposta = await fetch('/api/estoque', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ nome: nome, quantidade: qtd, unidade: unidade }) });
        if (!resposta.ok) throw new Error();
    } catch (e) { return mostrarToast('Erro ao conectar', 'erro'); }
    document.getElementById('materialNome').value = '';
    document.getElementById('materialQtd').value = '';
    mostrarToast('Material adicionado!');
    carregarEstoque();
}

function abrirModalEditarEstoque(id, nomeAtual, qtdAtual, unidadeAtual) {
    materialEditandoId = id;
    document.getElementById('editMaterialNome').value = nomeAtual;
    document.getElementById('editMaterialQtd').value = qtdAtual;
    document.getElementById('editMaterialUnidade').value = unidadeAtual;
    document.getElementById('modalEditarEstoque').style.display = 'flex';
}

function fecharModalEditarEstoque() { document.getElementById('modalEditarEstoque').style.display = 'none'; materialEditandoId = null; }

async function salvarEdicaoEstoque() {
    const novoNome = document.getElementById('editMaterialNome').value;
    const novaQtd = document.getElementById('editMaterialQtd').value;
    const novaUnidade = document.getElementById('editMaterialUnidade').value;
    if (!novoNome || !novaQtd) return mostrarToast('Preencha todos os campos!', 'erro');
    try { await fetch(`/api/estoque/${materialEditandoId}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ nome: novoNome, quantidade: novaQtd, unidade: novaUnidade }) });
    } catch (e) { return mostrarToast('Erro ao conectar', 'erro'); }
    fecharModalEditarEstoque();
    mostrarToast('Material atualizado!');
    carregarEstoque();
}

async function atualizarQuantidade(id_material, nova_qtd) {
    if (nova_qtd < 0) return;
    try { await fetch(`/api/estoque/${id_material}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ quantidade: nova_qtd }) }); carregarEstoque();
    } catch (e) { mostrarToast('Erro ao atualizar quantidade', 'erro'); }
}

async function deletarEstoque(id_material) {
    if (confirm("Deseja remover este material do estoque?")) {
        try { await fetch(`/api/estoque/${id_material}`, { method: 'DELETE' }); mostrarToast('Material removido!', 'erro'); carregarEstoque();
        } catch (e) { mostrarToast('Erro ao remover', 'erro'); }
    }
}

async function exportarPedidos() {
    try {
        const resposta = await fetch('/api/pedidos/exportar');
        if (!resposta.ok) throw new Error();
        const blob = await resposta.blob();
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = 'pedidos.xlsx';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (e) { mostrarToast('Erro ao exportar', 'erro'); }
}

async function exportarEstoque() {
    try {
        const resposta = await fetch('/api/estoque/exportar');
        if (!resposta.ok) throw new Error();
        const blob = await resposta.blob();
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = 'estoque.xlsx';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (e) { mostrarToast('Erro ao exportar', 'erro'); }
}