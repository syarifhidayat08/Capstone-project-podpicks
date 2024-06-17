package com.bangkit.podpicks.ui.home

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

data class HomeItem(val title: String, val children: List<String>)

class HomeViewModel : ViewModel() {

    private val _homeItems = MutableLiveData<List<HomeItem>>().apply {
        value = listOf(
            HomeItem("Parent 1", listOf("Child 1-1", "Child 1-2", "Child 1-3")),
            HomeItem("Parent 2", listOf("Child 2-1", "Child 2-2")),
            HomeItem("Parent 3", listOf("Child 3-1", "Child 3-2", "Child 3-3")),
            HomeItem("Parent 4", listOf("Child 4-1")),
            HomeItem("Parent 5", listOf("Child 5-1", "Child 5-2", "Child 5-3", "Child 5-4"))
        )
    }
    val parentItems: LiveData<List<HomeItem>> = _homeItems
}