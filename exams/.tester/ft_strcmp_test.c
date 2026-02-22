#include <stdio.h>
#include <string.h>

int	ft_strcmp(char *s1, char *s2);

static int	failed = 0;

static void	check_sign(int got, int expected_sign, const char *name)
{
	int	got_sign = (got > 0) - (got < 0);

	if (got_sign != expected_sign)
	{
		printf("FAIL [%s]: got sign %d, expected sign %d (value: %d)\n",
			name, got_sign, expected_sign, got);
		failed++;
	}
}

int	main(void)
{
	check_sign(ft_strcmp("", ""), 0, "empty==empty");
	check_sign(ft_strcmp("hello", "hello"), 0, "hello==hello");
	check_sign(ft_strcmp("abc", "abd"), -1, "abc<abd");
	check_sign(ft_strcmp("abd", "abc"), 1, "abd>abc");
	check_sign(ft_strcmp("abc", "ab"), 1, "abc>ab");
	check_sign(ft_strcmp("ab", "abc"), -1, "ab<abc");
	check_sign(ft_strcmp("A", "a"), -1, "A<a");
	check_sign(ft_strcmp("a", "A"), 1, "a>A");
	check_sign(ft_strcmp("z", "a"), 1, "z>a");
	check_sign(ft_strcmp("a", "z"), -1, "a<z");
	check_sign(ft_strcmp("42", "42"), 0, "42==42");
	check_sign(ft_strcmp("abc", ""), 1, "abc>empty");
	check_sign(ft_strcmp("", "abc"), -1, "empty<abc");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
