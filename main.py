import json
import os

# --- CLASSE TAREFA ---
class Tarefa:
    def __init__(self, descricao, concluida=False):
        # Atributos (estado do objeto)
        self.descricao = descricao
        self.concluida = concluida

    # Métodos (comportamento do objeto)
    def marcar_como_concluida(self):
        self.concluida = True

    def para_dicionario(self):
        """Converte o objeto para um dicionário para salvar em JSON."""
        return {"descricao": self.descricao, "concluida": self.concluida}

    @classmethod
    def de_dicionario(cls, dados):
        """Cria um objeto Tarefa a partir de um dicionário (Factory Method)."""
        return cls(dados["descricao"], dados["concluida"])


# --- CLASSE GERENCIADOR ---
class GerenciadorTarefas:
    def __init__(self, arquivo="tarefas.json"):
        self.arquivo = arquivo
        self.tarefas = [] # Lista que armazenará os objetos Tarefa
        self.carregar_dados()

    def adicionar_tarefa(self, descricao):
        nova_tarefa = Tarefa(descricao)
        self.tarefas.append(nova_tarefa)
        self.salvar_dados()
        print("\n✅ Tarefa adicionada com sucesso!")

    def listar_tarefas(self, filtro=None):
        """Lista tarefas diferenciando pendentes e concluídas. Aceita filtro opcional."""
        if not self.tarefas:
            print("\n📋 Sua lista de tarefas está vazia.")
            return

        print("\n--- SUAS TAREFAS ---")
        for i, tarefa in enumerate(self.tarefas):
            # Filtro extra (criatividade)
            if filtro == 'pendente' and tarefa.concluida: continue
            if filtro == 'concluida' and not tarefa.concluida: continue

            status = "[X]" if tarefa.concluida else "[ ]"
            print(f"{i} - {status} {tarefa.descricao}")
        print("--------------------")

    def concluir_tarefa(self, indice):
        if 0 <= indice < len(self.tarefas):
            self.tarefas[indice].marcar_como_concluida()
            self.salvar_dados()
            print("\n✅ Tarefa marcada como concluída!")
        else:
            print("\n❌ Índice inválido.")

    def remover_tarefa(self, indice):
        if 0 <= indice < len(self.tarefas):
            removida = self.tarefas.pop(indice)
            self.salvar_dados()
            print(f"\n🗑️ Tarefa '{removida.descricao}' removida!")
        else:
            print("\n❌ Índice inválido.")

    # --- PERSISTÊNCIA DE DADOS ---
    def salvar_dados(self):
        """Encapsula a lógica de salvar no arquivo (Persistência)."""
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            # Converte lista de objetos Tarefa para lista de dicionários
            dados = [t.para_dicionario() for t in self.tarefas]
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def carregar_dados(self):
        """Encapsula a lógica de carregar o arquivo."""
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                try:
                    dados = json.load(f)
                    # Recria os objetos Tarefa
                    self.tarefas = [Tarefa.de_dicionario(d) for d in dados]
                except json.JSONDecodeError:
                    self.tarefas = []


# --- INTERFACE CLI (MENU) ---
def main():
    gerenciador = GerenciadorTarefas()

    while True:
        print("\n" + "="*30)
        print("    GERENCIADOR DE TAREFAS")
        print("="*30)
        print("1. Adicionar nova tarefa")
        print("2. Listar todas as tarefas")
        print("3. Listar apenas pendentes (Extra)")
        print("4. Marcar tarefa como concluída")
        print("5. Remover tarefa")
        print("6. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            desc = input("Digite a descrição da tarefa: ")
            gerenciador.adicionar_tarefa(desc)
        elif opcao == '2':
            gerenciador.listar_tarefas()
        elif opcao == '3':
            gerenciador.listar_tarefas(filtro='pendente')
        elif opcao == '4':
            gerenciador.listar_tarefas()
            try:
                idx = int(input("Digite o número da tarefa para concluir: "))
                gerenciador.concluir_tarefa(idx)
            except ValueError:
                print("Por favor, digite um número válido.")
        elif opcao == '5':
            gerenciador.listar_tarefas()
            try:
                idx = int(input("Digite o número da tarefa para remover: "))
                gerenciador.remover_tarefa(idx)
            except ValueError:
                print("Por favor, digite um número válido.")
        elif opcao == '6':
            print("Saindo do sistema. Suas tarefas foram salvas. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()