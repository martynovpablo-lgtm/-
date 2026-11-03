"""№2: категория ағашын және шығындарын рекурсивті есептеу."""

from core.domain import Category, Transaction


def flatten_categories(cats: tuple[Category, ...], root: str) -> tuple[Category, ...]:
    """Root өзі және барлық ұрпағы (preorder); цикл анықталса ValueError."""
    lookup = {c.id: c for c in cats}

    def walk(node: str, path: frozenset) -> tuple:
        if node in path:
            raise ValueError("Категория иерархиясында цикл бар")
        if node not in lookup:
            return ()
        children = tuple(c.id for c in cats if c.parent_id == node)
        return (lookup[node],) + tuple(
            child for cid in children for child in walk(cid, path | frozenset((node,)))
        )

    return walk(root, frozenset())


def sum_expenses_recursive(
    cats: tuple[Category, ...], trans: tuple[Transaction, ...], root_id: str
) -> int:
    """Шығыс оң модуль ретінде; кірістер есепке алынбайды."""
    ids = frozenset(c.id for c in cats)

    def total(node: str, path: frozenset) -> int:
        if node in path:
            raise ValueError("Категория иерархиясында цикл бар")
        if node not in ids:
            return 0
        own = sum(-t.amount for t in trans if t.cat_id == node and t.amount < 0)
        return own + sum(
            total(c.id, path | frozenset((node,))) for c in cats if c.parent_id == node
        )

    return total(root_id, frozenset())
