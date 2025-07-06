from analise.sistema import SistemaAnaliseEngajamento


def main():

    def definir_top_n():
        while True:
            try:
                top_n = int(input("Digite o valor de N para os relatórios (ex: 5): "))
                if top_n > 0:
                    return top_n
                else:
                    print("Por favor, insira um número positivo.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número inteiro.")

    sistema = SistemaAnaliseEngajamento()
    sistema._carregar_interacoes_csv('interacoes_globo.csv')
    sistema.processar_interacoes_da_fila()

    def menu():
        print("\n\nMenu:")
        print("1. Gerar relatório de engajamento dos conteúdos")
        print("2. Gerar relatório de atividade dos usuários")
        print("3. Identificar top conteúdos por tempo total de consumo")
        print("4. Identificar top conteúdos por total de interações de engajamento")
        print("5. Identificar usuários com maior tempo total de consumo de conteúdo")
        print("6. Identificar plataformas com maior engajamento")
        print("7. Identificar conteúdos mais comentados")
        print("8. Identificar total de interações por tipo de conteúdo")
        print("9. Identificar tempo médio de consumo por plataforma")
        print("10. Identificar quantidade de comentários por conteúdo")
        print("0. Sair\n")
    while True:
        print("\nBem-vindo ao Sistema de Análise de Engajamento!")
        menu()
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            top_n = definir_top_n()
            print(f"Gerando relatório de engajamento dos conteúdos para os top {top_n} conteúdos...")
            sistema.gerar_relatorio_engajamento_conteudos(top_n=top_n)
        elif opcao == '2':
            top_n = definir_top_n()
            print(f"Gerando relatório de atividade dos usuários para os top {top_n} usuários...")
            sistema.gerar_relatorio_atividade_usuarios(top_n=top_n)
        elif opcao == '3':
            top_n = definir_top_n()
            print(f"Identificando os top conteúdos por tempo total de consumo para os top {top_n} conteúdos...")
            sistema.identificar_top_conteudos('calcular_tempo_total_consumo', n=top_n)
        elif opcao == '4':
            top_n = definir_top_n()
            print(f"Identificando os top conteúdos por total de interações de engajamento para os top {top_n} conteúdos...")
            sistema.identificar_top_conteudos('calcular_total_interacoes_engajamento', n=top_n)
        elif opcao == '5':
            top_n = definir_top_n()
            print(f"Identificando os usuários com maior tempo total de consumo de conteúdo para os top {top_n} usuários...")
            sistema.identificar_top_usuarios_tempo_consumo(top_n=top_n)
        elif opcao == '6':
            print("Identificando plataformas com maior engajamento...")
            top_n = definir_top_n()
            print(f"Para os top {top_n} plataformas, escolha o tipo de interação:")
            print("1. share \n2. like \n3. comment \n4. view_start \n5. Todos os tipos")
            while True:
                tipo_interacao = input("Escolha o tipo de interação (1, 2, 3 ou 4): ")
                if tipo_interacao in ['1', '2', '3', '4', '5']:
                    if tipo_interacao == '1':
                        sistema.identificar_top_plataformas(top_n=top_n, tipo_engajamento='share')
                    elif tipo_interacao == '2':
                        sistema.identificar_top_plataformas(top_n=top_n, tipo_engajamento='like')
                    elif tipo_interacao == '3':
                        sistema.identificar_top_plataformas(top_n=top_n, tipo_engajamento='comment')
                    elif tipo_interacao == '4':
                        sistema.identificar_top_plataformas(top_n=top_n, tipo_engajamento='view_start')
                    elif tipo_interacao == '5':
                        sistema.identificar_top_plataformas(top_n=top_n)

                    break
                else:
                    print("Opção inválida, tente novamente.")

        elif opcao == '7':
            top_n = definir_top_n()
            print(f"Identificando os conteúdos mais comentados para os top {top_n} conteúdos...")
            sistema.identificar_top_conteudos_comentados(top_n=top_n)
        elif opcao == '8':
            top_n = definir_top_n()
            print(f"Identificando o total de interações por tipo de conteúdo para os top {top_n} conteúdos...")
            sistema.identificar_total_interacoes_por_tipo_conteudo(top_n=top_n)
        elif opcao == '9':
            top_n = definir_top_n()
            print(f"Identificando o tempo médio de consumo por plataforma para os top {top_n} plataformas...")
            sistema.identificar_tempo_medio_consumo_por_plataforma(top_n=top_n)
        elif opcao == '10':
            top_n = definir_top_n()
            print(f"Identificando a quantidade de comentários por conteúdo para os top {top_n} conteúdos...")
            sistema.identificar_quantidade_comentarios_por_conteudo(top_n=top_n)
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")
    
    
    print("Programa encerrado.")
    
   
    
if __name__ == '__main__':
    main()