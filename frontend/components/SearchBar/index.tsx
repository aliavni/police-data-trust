"use client"

import { TextField, InputAdornment } from "@mui/material"
import { Search } from "@mui/icons-material"
import { useSearch } from "@/providers/SearchProvider"
import { useSearchParams } from "next/navigation"
import React from "react"

export const SearchBar = () => {
  const { searchAll } = useSearch()
  const searchParams = useSearchParams()

  const [localInput, setLocalInput] = React.useState(searchParams.get("query") || "")

  const handleSearch = async (query: string) => {
    console.log("Handling search for query:", query)
    await searchAll({ query })
  }

  return (
    <TextField
      variant="outlined"
      value={localInput}
      onChange={(e) => setLocalInput(e.target.value)}
      onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
          handleSearch(localInput)
        }
      }}
      sx={{
        maxWidth: "546px",
        width: "100%",
        "& fieldset": { borderRadius: "20px" },
        "& .MuiInputBase-input": {
          overflow: "hidden",
          textOverflow: "ellipsis"
        }
      }}
      placeholder="Search officer, unit, or agency"
      slotProps={{
        input: {
          startAdornment: (
            <InputAdornment position="start">
              <Search />
            </InputAdornment>
          )
        }
      }}
    />
  )
}

export default SearchBar
