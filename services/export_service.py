import pandas as pd
from tkinter import messagebox, filedialog


def exportar_produtos_excel(produtos):

    if not produtos:
        messagebox.showwarning("Aviso", "Nenhum produto para exportar.")
        return

    try:
        caminho = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel file", "*.xlsx")],
            title="Salvar relatório"
        )

        if not caminho:
            return

        dados = []

        for p in produtos:
            dados.append({
                "ID": p["id"],
                "Nome": p["nome"],
                "Categoria": p["categoria"],
                "Fornecedor": p["fornecedor"],
                "Preço": p["preco"],
                "Quantidade": p["quantidade"],
                "Estoque Mínimo": p["estoque_minimo"]
            })

        df = pd.DataFrame(dados)

        df.to_excel(caminho, index=False)

        messagebox.showinfo(
            "Sucesso",
            "Arquivo Excel gerado com sucesso!"
        )

    except Exception as e:
        messagebox.showerror(
            "Erro",
            str(e)
        )
