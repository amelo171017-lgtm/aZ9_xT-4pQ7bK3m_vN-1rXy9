class SistemaConsulta {
    constructor() {
        this.categoriasSelecionadas = new Set();
        this.dados = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkAuth();
    }

    bindEvents() {
        document.getElementById('login-form').addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('logout-btn').addEventListener('click', () => this.logout());
        document.getElementById('buscar-btn').addEventListener('click', () => this.buscarCodigos());
        document.getElementById('ver-dados-btn').addEventListener('click', () => this.verDadosCompletos());
        document.getElementById('close-modal').addEventListener('click', () => this.fecharModal());
        document.getElementById('copy-id-btn').addEventListener('click', () => this.copiarId());
        document.getElementById('copy-message-btn').addEventListener('click', () => this.copiarMensagem());
        
        document.addEventListener('click', (e) => {
            const categoryItem = e.target.closest('.category-item');
            if (categoryItem) {
                this.toggleCategoria(categoryItem.dataset.categoria);
            }
        });
    }

    async handleLogin(e) {
        e.preventDefault();
        const senha = document.getElementById('senha').value;
        
        try {
            const response = await fetch('/verificar_senha', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ senha })
            });
            
            const data = await response.json();
            
            if (data.sucesso) {
                this.showMessage(data.mensagem, 'success');
                setTimeout(() => {
                    this.showMainScreen();
                    this.carregarDados();
                }, 1000);
            } else {
                this.showMessage(data.mensagem, 'error');
            }
        } catch (error) {
            this.showMessage('Erro de conexão', 'error');
        }
    }

    async carregarDados() {
        try {
            const response = await fetch('/carregar_dados', {
                credentials: 'include'
            });
            const data = await response.json();
            
            if (response.ok) {
                this.dados = data;
                this.atualizarInterface();
            } else {
                this.showMessage(data.erro, 'error');
            }
        } catch (error) {
            this.showMessage('Erro ao carregar dados', 'error');
        }
    }

    atualizarInterface() {
        document.getElementById('total-registros').textContent = this.dados.total_registros;
        document.getElementById('total-campos').textContent = this.dados.total_campos;
        
        this.renderizarCategorias();
    }

    renderizarCategorias() {
        const container = document.getElementById('categories-list');
        container.innerHTML = '';
        
        this.dados.categorias.forEach(categoria => {
            const item = document.createElement('div');
            item.className = 'category-item';
            item.dataset.categoria = categoria;
            
            const checkbox = document.createElement('div');
            checkbox.className = 'category-checkbox';
            if (this.categoriasSelecionadas.has(categoria)) {
                checkbox.classList.add('checked');
            }
            
            const label = document.createElement('span');
            label.className = 'category-label';
            label.textContent = categoria;
            
            item.appendChild(checkbox);
            item.appendChild(label);
            container.appendChild(item);
        });
    }

    toggleCategoria(categoria) {
        if (this.categoriasSelecionadas.has(categoria)) {
            this.categoriasSelecionadas.delete(categoria);
        } else {
            this.categoriasSelecionadas.add(categoria);
        }
        
        this.renderizarCategorias();
        this.atualizarBotaoBusca();
    }

    atualizarBotaoBusca() {
        const btnBuscar = document.getElementById('buscar-btn');
        btnBuscar.disabled = this.categoriasSelecionadas.size === 0;
    }

    async buscarCodigos() {
        if (this.categoriasSelecionadas.size === 0) {
            this.showMessage('Selecione pelo menos uma categoria', 'warning');
            return;
        }

        try {
            const response = await fetch('/buscar_codigos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ 
                    categorias: Array.from(this.categoriasSelecionadas) 
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.mostrarResultados(data);
            } else {
                this.showMessage(data.erro, 'error');
            }
        } catch (error) {
            this.showMessage('Erro na busca', 'error');
        }
    }

    mostrarResultados(data) {
        const container = document.getElementById('results-container');
        const content = document.getElementById('results-content');
        const copyIdBtn = document.getElementById('copy-id-btn');
        const copyMessageBtn = document.getElementById('copy-message-btn');
        
        content.innerHTML = '';
        
        if (data.total_encontrados > 0) {
            const summary = document.createElement('div');
            summary.className = 'result-summary';
            summary.innerHTML = `
                <p><strong>Categorias selecionadas:</strong> ${data.categorias_buscadas.join(', ')}</p>
                <p><strong>Total encontrado:</strong> ${data.total_encontrados} código(s)</p>
            `;
            content.appendChild(summary);
            
            data.codigos.forEach(codigo => {
                const item = document.createElement('div');
                item.className = 'result-item';
                item.textContent = codigo;
                content.appendChild(item);
            });
            
            // Mostrar botões de copiar
            copyIdBtn.style.display = 'inline-block';
            copyMessageBtn.style.display = 'inline-block';
            
            // Armazenar os códigos para uso nos botões
            this.codigosEncontrados = data.codigos;
            console.log('Códigos armazenados:', this.codigosEncontrados);
        } else {
            content.innerHTML = `
                <div class="no-results">
                    <p>Nenhum código encontrado para as categorias selecionadas.</p>
                    <p><em>Dica: Tente selecionar menos categorias para ampliar os resultados.</em></p>
                </div>
            `;
            
            // Ocultar botões de copiar
            copyIdBtn.style.display = 'none';
            copyMessageBtn.style.display = 'none';
        }
        
        container.classList.remove('hidden');
    }

    verDadosCompletos() {
        if (!this.dados) return;
        
        const modal = document.getElementById('data-modal');
        const container = document.getElementById('data-table-container');
        
        const table = document.createElement('table');
        table.className = 'data-table';
        
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        
        this.dados.colunas.forEach(coluna => {
            const th = document.createElement('th');
            th.textContent = coluna;
            headerRow.appendChild(th);
        });
        
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        const tbody = document.createElement('tbody');
        
        this.dados.dados.forEach(registro => {
            const row = document.createElement('tr');
            
            this.dados.colunas.forEach(coluna => {
                const td = document.createElement('td');
                td.textContent = registro[coluna] || '';
                row.appendChild(td);
            });
            
            tbody.appendChild(row);
        });
        
        table.appendChild(tbody);
        container.innerHTML = '';
        container.appendChild(table);
        
        modal.classList.remove('hidden');
    }

    fecharModal() {
        document.getElementById('data-modal').classList.add('hidden');
    }

    showMainScreen() {
        document.getElementById('login-screen').classList.remove('active');
        document.getElementById('main-screen').classList.add('active');
    }

    logout() {
        fetch('/logout', { credentials: 'include' }).then(() => {
            this.categoriasSelecionadas.clear();
            this.dados = null;
            
            document.getElementById('main-screen').classList.remove('active');
            document.getElementById('login-screen').classList.add('active');
            document.getElementById('senha').value = '';
            document.getElementById('results-container').classList.add('hidden');
            
            this.showMessage('Sessão encerrada', 'info');
        });
    }

    checkAuth() {
        if (document.getElementById('main-screen').classList.contains('active')) {
            this.carregarDados();
        }
    }

    showMessage(message, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${type}`;
        messageDiv.textContent = message;
        
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }

    async copiarId() {
        console.log('Copiar ID chamado');
        console.log('Códigos encontrados:', this.codigosEncontrados);
        
        if (!this.codigosEncontrados || this.codigosEncontrados.length === 0) {
            this.showMessage('Nenhum código disponível para copiar', 'warning');
            return;
        }

        try {
            const codigos = this.codigosEncontrados.join('\n');
            console.log('Texto a copiar:', codigos);
            
            if (navigator.clipboard && window.isSecureContext) {
                await navigator.clipboard.writeText(codigos);
                this.showMessage('Códigos copiados para a área de transferência!', 'success');
            } else {
                this.copiarTextoFallback(codigos);
            }
        } catch (error) {
            console.error('Erro ao copiar:', error);
            this.copiarTextoFallback(this.codigosEncontrados.join('\n'));
        }
    }

    async copiarMensagem() {
        if (!this.codigosEncontrados || this.codigosEncontrados.length === 0) {
            this.showMessage('Nenhum código disponível para copiar', 'warning');
            return;
        }

        try {
            const mensagem = `🎉 *Obrigado por comprar conosco!*\n\n${this.codigosEncontrados.join('\n')}`;
            
            if (navigator.clipboard && window.isSecureContext) {
                await navigator.clipboard.writeText(mensagem);
                this.showMessage('Mensagem copiada para a área de transferência!', 'success');
            } else {
                this.copiarTextoFallback(mensagem);
            }
        } catch (error) {
            this.copiarTextoFallback(`🎉 *Obrigado por comprar conosco!*\n\n${this.codigosEncontrados.join('\n')}`);
        }
    }

    copiarTextoFallback(texto) {
        const textArea = document.createElement('textarea');
        textArea.value = texto;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            this.showMessage('Códigos copiados para a área de transferência!', 'success');
        } catch (error) {
            this.showMessage('Erro ao copiar. Tente selecionar e copiar manualmente.', 'error');
        }
        
        document.body.removeChild(textArea);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new SistemaConsulta();
});

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js');
    });
}
