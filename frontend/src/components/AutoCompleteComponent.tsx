import React, { useState } from "react";
// @ts-ignore
import Autosuggest from "react-autosuggest";

const AutoCompleteComponent = ({ onSongSelect }: {onSongSelect: any}) => {
  const [value, setValue] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  const getSuggestions = async (inputValue: string) => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/search?q=${inputValue}`
      );
      const data = await response.json();
      return data.suggestions;
    } catch (error) {
      console.error("Error fetching suggestions:", error);
      return [];
    }
  };
// @ts-ignore
  const onSuggestionsFetchRequested = async ({ value }) => {
    const suggestions = await getSuggestions(value);
    setSuggestions(suggestions);
  };

  const onSuggestionsClearRequested = () => {
    setSuggestions([]);
  };

// @ts-ignore
  const onSuggestionSelected = (event, { suggestion }) => {
    console.log("Selected suggestion:", suggestion);
    onSongSelect(suggestion.title); // Pass the selected title back to the parent component
  };

  const inputProps = {
    placeholder: "Search for a song",
    value,
    // @ts-ignore
    onChange: (_, { newValue }) => setValue(newValue),
  };

  return (
    <Autosuggest
      suggestions={suggestions}
      onSuggestionsFetchRequested={onSuggestionsFetchRequested}
      onSuggestionsClearRequested={onSuggestionsClearRequested}
      onSuggestionSelected={onSuggestionSelected}
      // @ts-ignore
      getSuggestionValue={(suggestion) => suggestion.title}
      // @ts-ignore
      renderSuggestion={(suggestion) => <div>{suggestion.title}</div>}
      inputProps={inputProps}
    />
  );
};

export default AutoCompleteComponent;
