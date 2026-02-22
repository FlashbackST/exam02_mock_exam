#include <stdio.h>
#include <string.h>

char	*ft_strpbrk(const char *s1, const char *s2);

static int	failed = 0;

static void	check(const char *got, const char *expected, const char *name)
{
	if (got == NULL && expected == NULL)
		return;
	if (got == NULL || expected == NULL || strcmp(got, expected) != 0)
	{
		printf("FAIL [%s]: got \"%s\", expected \"%s\"\n",
			name,
			got ? got : "NULL",
			expected ? expected : "NULL");
		failed++;
	}
}

int	main(void)
{
	char	s1[] = "hello world";
	char	s2[] = "abcdef";
	char	s3[] = "12345";
	char	s4[] = "hello";

	check(ft_strpbrk(s1, "aeiou"), s1 + 1, "first vowel in hello world");
	check(ft_strpbrk(s1, " "), s1 + 5, "space");
	check(ft_strpbrk(s1, "xyz"), NULL, "no match");
	check(ft_strpbrk("", "abc"), NULL, "empty s1");
	check(ft_strpbrk(s2, ""), NULL, "empty s2");
	check(ft_strpbrk(s2, "d"), s2 + 3, "d in abcdef");
	check(ft_strpbrk(s3, "13"), s3, "1 first");
	check(ft_strpbrk(s4, "h"), s4, "first char");
	check(ft_strpbrk(s4, "o"), s4 + 4, "last char");
	check(ft_strpbrk("abc", "cba"), (char *)"abc", "first of abc");
	check(ft_strpbrk("hello", "xyz"), NULL, "no match hello");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
