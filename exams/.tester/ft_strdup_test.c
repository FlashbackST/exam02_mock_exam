#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char	*ft_strdup(char *src);

static int	failed = 0;

static void	check(char *src, const char *name)
{
	char	*dup = ft_strdup(src);

	if (dup == NULL)
	{
		printf("FAIL [%s]: returned NULL\n", name);
		failed++;
		return;
	}
	if (dup == src)
	{
		printf("FAIL [%s]: returned same pointer (not a copy)\n", name);
		failed++;
		free(dup);
		return;
	}
	if (strcmp(dup, src) != 0)
	{
		printf("FAIL [%s]: got \"%s\", expected \"%s\"\n", name, dup, src);
		failed++;
	}
	free(dup);
}

int	main(void)
{
	check("hello", "hello");
	check("", "empty");
	check("a", "single char");
	check("Hello World", "with space");
	check("42", "42");
	check("abcdefghijklmnopqrstuvwxyz", "alphabet");
	check("!@#$%^&*()", "special");
	check("   spaces   ", "spaces");
	check("\t\n\r", "escapes");
	check("0123456789", "digits");
	check("longstringtotestduplicationcorrectly", "long string");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
