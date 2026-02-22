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

void	ft_list_remove_if(t_list **begin_list, void *data_ref, int (*cmp)());

static int	failed = 0;

/* cmp must return 0 when data are equal (per subject spec) */
static int	cmp_int(void *a, void *b)
{
	return ((int)(long)a - (int)(long)b);
}

static t_list	*make_node(int val, t_list *next)
{
	t_list	*node = malloc(sizeof(t_list));
	node->data = (void *)(long)val;
	node->next = next;
	return (node);
}

static int	list_len(t_list *lst)
{
	int	n = 0;
	while (lst) { n++; lst = lst->next; }
	return (n);
}

static void	free_list(t_list *lst)
{
	t_list	*tmp;
	while (lst) { tmp = lst->next; free(lst); lst = tmp; }
}

int	main(void)
{
	t_list	*lst;

	lst = make_node(1, make_node(2, make_node(3, NULL)));
	ft_list_remove_if(&lst, (void *)2L, cmp_int);
	if (list_len(lst) != 2 || (int)(long)lst->data != 1 || (int)(long)lst->next->data != 3)
	{ printf("FAIL [remove middle]: len=%d, head=%d\n", list_len(lst), (int)(long)lst->data); failed++; }
	free_list(lst);

	lst = make_node(1, make_node(2, make_node(3, NULL)));
	ft_list_remove_if(&lst, (void *)1L, cmp_int);
	if (list_len(lst) != 2 || (int)(long)lst->data != 2)
	{ printf("FAIL [remove head]: len=%d\n", list_len(lst)); failed++; }
	free_list(lst);

	lst = make_node(1, make_node(2, make_node(3, NULL)));
	ft_list_remove_if(&lst, (void *)3L, cmp_int);
	if (list_len(lst) != 2)
	{ printf("FAIL [remove tail]: len=%d\n", list_len(lst)); failed++; }
	free_list(lst);

	lst = make_node(2, make_node(1, make_node(2, make_node(2, NULL))));
	ft_list_remove_if(&lst, (void *)2L, cmp_int);
	if (list_len(lst) != 1 || (int)(long)lst->data != 1)
	{ printf("FAIL [remove all 2s]: len=%d\n", list_len(lst)); failed++; }
	free_list(lst);

	lst = NULL;
	ft_list_remove_if(&lst, (void *)1L, cmp_int);
	if (lst != NULL)
	{ printf("FAIL [remove from NULL]: list not NULL\n"); failed++; }

	lst = make_node(1, make_node(2, NULL));
	ft_list_remove_if(&lst, (void *)5L, cmp_int);
	if (list_len(lst) != 2)
	{ printf("FAIL [remove non-existing]: len=%d\n", list_len(lst)); failed++; }
	free_list(lst);

	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
