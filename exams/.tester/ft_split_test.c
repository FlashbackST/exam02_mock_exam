#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char	**ft_split(char *str);

static int	failed = 0;

static void	free_split(char **tab)
{
	int	i;

	if (!tab)
		return;
	i = 0;
	while (tab[i])
		free(tab[i++]);
	free(tab);
}

static void	check(char *str, int expected_count, const char **expected_words, const char *name)
{
	char	**result = ft_split(str);
	int		i;

	if (result == NULL && expected_count == 0)
		return;
	if (result == NULL)
	{
		printf("FAIL [%s]: returned NULL, expected %d words\n", name, expected_count);
		failed++;
		return;
	}
	i = 0;
	while (result[i])
		i++;
	if (i != expected_count)
	{
		printf("FAIL [%s]: got %d words, expected %d\n", name, i, expected_count);
		failed++;
		free_split(result);
		return;
	}
	i = 0;
	while (i < expected_count)
	{
		if (strcmp(result[i], expected_words[i]) != 0)
		{
			printf("FAIL [%s]: word[%d] got \"%s\", expected \"%s\"\n",
				name, i, result[i], expected_words[i]);
			failed++;
			free_split(result);
			return;
		}
		i++;
	}
	free_split(result);
}

int	main(void)
{
	const char	*w1[] = {"hello", "world"};
	const char	*w2[] = {"one"};
	const char	*w3[] = {"a", "b", "c"};
	const char	*w4[] = {"hello", "world", "42"};
	const char	*w5[] = {"word"};
	const char	*w6[] = {"foo", "bar", "baz"};

	check("hello world", 2, w1, "hello world");
	check("one", 1, w2, "single word");
	check("a b c", 3, w3, "a b c");
	check("   hello   world   42   ", 3, w4, "extra spaces");
	check("", 0, NULL, "empty string");
	check("   ", 0, NULL, "spaces only");
	check("word", 1, w5, "single word no spaces");
	check("foo  bar  baz", 3, w6, "double spaces");
	check("\thello\tworld", 2, w1, "tabs");
	check("\nhello\nworld\n", 2, w1, "newlines");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
