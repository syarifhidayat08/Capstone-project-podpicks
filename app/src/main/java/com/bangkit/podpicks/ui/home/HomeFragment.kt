package com.bangkit.podpicks.ui.home

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.Observer
import androidx.recyclerview.widget.LinearLayoutManager
import com.bangkit.podpicks.adapter.HomeAdapter
import com.bangkit.podpicks.databinding.FragmentHomeBinding

class HomeFragment : Fragment() {

    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!
    private val homeViewModel: HomeViewModel by viewModels()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        val view = binding.root

        // Initialize RecyclerView
        val recyclerView = binding.rvHome
        recyclerView.layoutManager = LinearLayoutManager(context)

        // Observe ViewModel data
        homeViewModel.parentItems.observe(viewLifecycleOwner, Observer { homeItems ->
            recyclerView.adapter = HomeAdapter(homeItems)
        })

        return view
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}