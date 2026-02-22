#include <stdio.h>
#include <string.h>
#include <unistd.h>

void	ft_putstr(char *str);

int	main(void)
{
	/* ft_putstr uses write() so we just test it outputs correctly
	   We redirect stdout and compare manually via the shell tester.
	   Here we just call it and verify it doesn't crash. */

	ft_putstr("hello");
	ft_putstr("\n");
	ft_putstr("world\n");
	ft_putstr("\n");
	ft_putstr("42\n");
	ft_putstr("\n");
	ft_putstr("abc\n");
	ft_putstr("\n");
	ft_putstr("test string\n");
	ft_putstr("\n");
	printf("ALL TESTS PASSED\n");
	return (0);
}
