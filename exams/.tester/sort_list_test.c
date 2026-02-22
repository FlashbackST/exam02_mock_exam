#include <stdio.h>
#include <stdlib.h>

#ifndef FT_LIST_H
# define FT_LIST_H
typedef struct s_list
{
	struct s_list	*next;
	void			*data;
}	t_list;
#endif

t_list	*sort_list(t_list *lst, int (*cmp)(int, int));

static int	failed = 0;

static int	cmp_asc(int a, int b)
{
	return (a <= b);
}

static t_list	*make_node(int val, t_list *next)
{
	t_list	*node = malloc(sizeof(t_list));

	node->data = (void *)(long)val;
	node->next = next;
	return (node);
}

static void	free_list(t_list *lst)
{
	t_list	*tmp;

	while (lst)
	{
		tmp = lst->next;
		free(lst);
		lst = tmp;
	}
}

static void	check_sorted(t_list *lst, const char *name)
{
	while (lst && lst->next)
	{
		if ((long)lst->data > (long)lst->next->data)
		{
			printf("FAIL [%s]: not sorted\n", name);
			failed++;
			return;
		}
		lst = lst->next;
	}
}

int	main(void)
{
	t_list	*lst;

	lst = make_node(3, make_node(1, make_node(2, NULL)));
	lst = sort_list(lst, cmp_asc);
	check_sorted(lst, "3,1,2");
	free_list(lst);

	lst = make_node(1, make_node(2, make_node(3, NULL)));
	lst = sort_list(lst, cmp_asc);
	check_sorted(lst, "already sorted");
	free_list(lst);

	lst = make_node(5, make_node(4, make_node(3, make_node(2, make_node(1, NULL)))));
	lst = sort_list(lst, cmp_asc);
	check_sorted(lst, "reverse 5 elems");
	free_list(lst);

	lst = make_node(42, NULL);
	lst = sort_list(lst, cmp_asc);
	check_sorted(lst, "single element");
	free_list(lst);

	lst = make_node(2, make_node(1, NULL));
	lst = sort_list(lst, cmp_asc);
	check_sorted(lst, "two elements");
	free_list(lst);

	lst = make_node(5, make_node(5, make_node(5, NULL)));
	lst = sort_list(lst, cmp_asc);
	check_sorted(lst, "all same");
	free_list(lst);

	lst = sort_list(NULL, cmp_asc);
	if (lst != NULL)
	{
		printf("FAIL [NULL list]: expected NULL return\n");
		failed++;
	}

	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
