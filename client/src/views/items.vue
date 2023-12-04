<script setup>
import axios from 'axios'
import { onMounted, computed, ref } from 'vue';

const items = ref([])
const searchText = ref('')
const loading = ref(false)

onMounted(async () => {

    const { data } = await axios.get('http://localhost:8000/api/items')
    items.value = data.results
    console.log(items.value)
})

const searchItem = async () => {
    // loading.value = true
    // const { data } = await axios.get(`http://localhost:8000/api/items?search=${searchText.value}`)
    // items.value = data.results
    // loading.value = false
    console.log('Called search item ', searchText.value)
}

// const filteredItems = computed(() => {
//     return items.value.filter(item => {
//         return item.title.toLowerCase().includes(searchText.value.toLowerCase())
//     })
// })

// filter based on regex
const filteredItems = computed(() => {
  
    let firstCharacter = searchText.value.substring(0, 1)
    let lastCharacter = searchText.value.substring(searchText.value.length - 1, searchText.value.length)
    // regex match first and last character
    console.log(firstCharacter, lastCharacter)
    const regex = new RegExp(`^${firstCharacter}.*${lastCharacter}$`, 'i')
    
    // const regex = new RegExp(searchText.value, 'i')
    return items.value.filter(item => {
      return item.title.match(regex)
    })
})

</script>

<template>
  <div class="container mx-auto bg-red-700 text-white px-3 py-2">
    <div class="flex flex-row">
      <input type="text" v-model="searchText" class="border-2 border-gray-300 w-2/3 mr-4 bg-green-700 h-10 px-5 pr-16 rounded-lg text-sm focus:outline-none" placeholder="Search" />
      <button @click="searchItem" class="bg-green-500 hover:bg-green-800 text-white font-bold py-2 px-4 rounded">
        Search
      </button>
    </div>
  </div>
  <div class="flex flex-col">
    <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
      <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
        <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="flex flex-col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ID
                  <input type="text" />
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Title
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Brand
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Discount
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Price
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Rating
                </th>
                <th scope="col" class="relative px-6 py-3">
                  <span class="sr-only">Edit</span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, itemIndex) in filteredItems" :key="item.id" :class="item.id % 2 === 0 ? 'bg-white' : 'bg-gray-50'">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {{ item.id }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ item.title }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ item.brand }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ item.discount }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ item.price }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ item.rating }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <a href="#" class="text-indigo-600 hover:text-indigo-900">Edit</a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
