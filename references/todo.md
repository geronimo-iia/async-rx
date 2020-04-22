

Select, better known as a map function, modifies an Observable<A> into Observable<B> given a function with the type A->B. For example, if we take the function x => 10 ∗ x and a list of 1,2,3. The result is 10,20,30, see figure 4. Note that this function did not change the type of the Observable but did change the values.

One of the most important operators in Rx is SelectMany, alias flatMap or mergeMap. SelectMany allows asynchronous queries, resulting in an observable of observables and it flattens the results, see figure 5. There may be multiple inner observables that run simultaneously, so the results from these inner observables may be intertwined.

The Where operators, alias filter, filters elements based on a condition. See figure 6.

Delay will project the sequence unmodified, but shifted into the future with a specified
delay.

Merge and Concat combine multiple sequences into one. Merge might interweave elements from different sequence whereas Concat emits all elements from the first sequence before turning to the next one.

Buffer and Window collect elements from the source sequence and emit them in groups. Buffer projects these elements onto arrays and emits those arrays when the buffer is closed. Window emits these elements in nested observables. It will emit a new inner observable when a window opens and will complete the inner observable when the window closes. Notice that there can be overlap between multiple buffers and windows if the next one opens before the last one closes. For example Buffer with a count of 2 and a skip of 1 will emit the last 2 elements (count 2) for every element (skip 1), so the sequence -1-2-3-4-| becomes --[12][23][34][4]|.

Similar to Window, GroupBy projects the sequence onto a number of inner observables but as opposite to Window where all windows receive the same sequence, GroupBy will emit elements only to one inner observable that is associated with the current element based on a key selector function. See figure 7.


The Amb operator (stands for ambiguous), alias race, subscribes to a number of observables and retrieves the first observable that yields a value, closing off all others. For example, Amb can automatically select the best server to download from: Amb listens to both servers and the first server that replies is used. See figure 8.


The following three operators, Debounce, Sample and Throttle are used to rate-limit the sequence. They will filter out elements based on the timing. There is a difference in how they exactly do that. Debounce will delay a value when it arrives and only emits the last value in a burst of events after the set delay is over and no new event arrives during this delay. Throttle will emit the first event from a burst and will ignore all subsequent values that arrive during the set timeout. Sample will emit the latest value on a set interval or emit nothing if no new value arrived during the last interval.

