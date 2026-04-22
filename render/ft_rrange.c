
int	*ft_rrange(int start, int end)
{
    int size = abs(end - start) + 1;
    int *arr;
    int step;
    int i = 0;

    arr = malloc(sizeof(int) * size);

    if (end > start)
        step = -1;
    else
        step = 1;

    while (i < size)
    {
        arr[i] = end;
        end += step;
        i++;
    }
    return arr;
}