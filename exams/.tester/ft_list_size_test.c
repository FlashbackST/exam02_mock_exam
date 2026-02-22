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

int	ft_list_size(t_list *begin_list);

static int	failed = 0;

static void	check(int got, int expected, const char *name)
{
	if (got != expected)
	{
		printf("FAIL [%s]: got %d, expected %d\n", name, got, expected);
		failed++;
	}
}

static t_list	*make_node(void *data, t_list *next)
{
	t_list	*node = malloc(sizeof(t_list));

	node->data = data;
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

int	main(void)
{
	t_list	*l1;
	t_list	*l2;
	t_list	*l3;
	t_list	*l5;

	check(ft_list_size(NULL), 0, "NULL list");

	l1 = make_node(NULL, NULL);
	check(ft_list_size(l1), 1, "1 element");
	free_list(l1);

	l2 = make_node(NULL, make_node(NULL, NULL));
	check(ft_list_size(l2), 2, "2 elements");
	free_list(l2);

	l3 = make_node(NULL, make_node(NULL, make_node(NULL, NULL)));
	check(ft_list_size(l3), 3, "3 elements");
	free_list(l3);

	l5 = make_node(NULL, make_node(NULL,
		make_node(NULL, make_node(NULL, make_node(NULL, NULL)))));
	check(ft_list_size(l5), 5, "5 elements");
	free_list(l5);

	t_list *l10 = NULL;
	int i = 0;
	while (i < 10)
	{
		t_list *n = make_node(NULL, l10);
		l10 = n;
		i++;
	}
	check(ft_list_size(l10), 10, "10 elements");
	free_list(l10);

	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
