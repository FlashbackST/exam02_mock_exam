#include <stdio.h>
#include <string.h>

char	*ft_strcpy(char *s1, char *s2);

static int	failed = 0;

static void	check_str(char *got, char *expected, const char *name)
{
	if (strcmp(got, expected) != 0)
	{
		printf("FAIL [%s]: got \"%s\", expected \"%s\"\n", name, got, expected);
		failed++;
	}
}

static void	check_ptr(char *got, char *dest, const char *name)
{
	if (got != dest)
	{
		printf("FAIL [%s]: return value is not dest\n", name);
		failed++;
	}
}

int	main(void)
{
	char	buf[64];
	char	*ret;

	ret = ft_strcpy(buf, "hello");
	check_str(buf, "hello", "basic copy");
	check_ptr(ret, buf, "return value basic");

	ft_strcpy(buf, "");
	check_str(buf, "", "empty string");

	ft_strcpy(buf, "42");
	check_str(buf, "42", "short string");

	ft_strcpy(buf, "Hello World!");
	check_str(buf, "Hello World!", "with space");

	ft_strcpy(buf, "abcdefghijklmnopqrstuvwxyz");
	check_str(buf, "abcdefghijklmnopqrstuvwxyz", "alphabet");

	ft_strcpy(buf, "\t\n\r");
	check_str(buf, "\t\n\r", "escape chars");

	ft_strcpy(buf, "!@#$%^&*()");
	check_str(buf, "!@#$%^&*()", "special chars");

	ft_strcpy(buf, "   spaces   ");
	check_str(buf, "   spaces   ", "spaces");

	ret = ft_strcpy(buf, "test");
	check_ptr(ret, buf, "return value test");

	ft_strcpy(buf, "0123456789");
	check_str(buf, "0123456789", "digits");

	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
