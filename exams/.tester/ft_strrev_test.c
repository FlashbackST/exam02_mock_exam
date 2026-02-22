#include <stdio.h>
#include <string.h>

char	*ft_strrev(char *str);

static int	failed = 0;

static void	check(char *got, char *expected, char *ret, char *orig, const char *name)
{
	if (strcmp(got, expected) != 0)
	{
		printf("FAIL [%s]: got \"%s\", expected \"%s\"\n", name, got, expected);
		failed++;
		return;
	}
	if (ret != orig)
	{
		printf("FAIL [%s]: return value is not the input pointer\n", name);
		failed++;
	}
}

int	main(void)
{
	char	s1[] = "hello";
	char	s2[] = "";
	char	s3[] = "a";
	char	s4[] = "ab";
	char	s5[] = "abc";
	char	s6[] = "42 school";
	char	s7[] = "racecar";
	char	s8[] = "Hello World";
	char	s9[] = "0123456789";
	char	s10[] = "!@#$";

	check(ft_strrev(s1), "olleh", s1, s1, "hello");
	check(ft_strrev(s2), "", s2, s2, "empty");
	check(ft_strrev(s3), "a", s3, s3, "single char");
	check(ft_strrev(s4), "ba", s4, s4, "two chars");
	check(ft_strrev(s5), "cba", s5, s5, "abc");
	check(ft_strrev(s6), "loohcs 24", s6, s6, "42 school");
	check(ft_strrev(s7), "racecar", s7, s7, "palindrome");
	check(ft_strrev(s8), "dlroW olleH", s8, s8, "Hello World");
	check(ft_strrev(s9), "9876543210", s9, s9, "digits");
	check(ft_strrev(s10), "$#@!", s10, s10, "special chars");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
