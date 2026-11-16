def display(x):
    try:
        import pandas as pd
        if isinstance(x, pd.DataFrame):
            with pd.option_context('display.width',250,'display.max_columns',20,'display.max_colwidth',40): print(x)
            return
    except Exception: pass
    print(x)
def Markdown(s): return s
